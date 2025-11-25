from model_text_gen import LocalInstructGenerator
from openai_text_gen import OpenAIInstructGenerator
import openai_text_gen as opn
import model_text_gen as mtg
import torch 
import json 
from tqdm import tqdm 
import argparse
from pymongo import MongoClient


def str2bool(v):
    """
    Convert string input to boolean (useful for argparse).
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', '1', 'y'):
        return True
    elif v.lower() in ('no', 'false', 'f', '0', 'n'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

with open("./data/profiles.json", 'r') as infile:
    jprofile = json.load(infile)

profiles = jprofile['profiles']

open_model_name = "mistralai/Mistral-7B-Instruct-v0.3"
# "meta-llama/Meta-Llama-3.1-8B-Instruct"
closed_model_name = "gpt-4o-mini"

open_model = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example: boolean CLI parameter")

    parser.add_argument(
        "--open_model",
        type=str2bool,
        nargs='?',
        const=True,
        default=False,
        help="Use open model? (True/False)"
    )
    args = parser.parse_args()

    open_model = args.open_model

    if open_model:
        model_name = open_model_name

        cfg = mtg.GenConfig(
            model_id=model_name, 
            device_map="auto",
            dtype=torch.float16,
            load_in_4bit=False,  # set True if you need to fit on smaller GPU
            max_new_tokens=140,
            temperature=0.9,
            top_p=0.92,
            top_k=40,
            repetition_penalty=1.05,
            seed=1234,
            stop_sequences=["</s>"]
        )

        gen = LocalInstructGenerator(cfg)

    else:
        model_name = closed_model_name
        apikeys = "/Users/Flint/Data/apikeys/keys.json"
        with open(apikeys, 'r') as inputdata:
            K = json.load(inputdata)
            api_key = K['openai']
        cfg = opn.GenConfig(
            model="gpt-4o-mini",   # or another suitable small model per your account availability
            max_new_tokens=140,
            temperature=0.9,
            top_p=0.92,
            seed=1234,
        )
        gen = OpenAIInstructGenerator(cfg, api_key=api_key)

    system_prompt = (
        "Agisci come una persona reale italiana. Rispetta rigorosamente il ruolo e lo stile indicati. "
    )
    instruction = "Scrivi un breve testo sulle cose importanti della vita"

    db = MongoClient()['gentext']['ita']
    collection = []
    counter = 0
    buffer = 20

    pfiles = set(db.distinct('profile_id'))

    for profile in tqdm(profiles):

        metadata = profile['metadata']
        profile_id = metadata['id']
        age_class = metadata['age_class']
        role = profile['data']

        if profile_id in pfiles:
            pass 
        else:
            counter += 1
            samples = gen.generate_role_texts(
                role=role,
                instruction=instruction,
                n_samples=2
            )
            for i, s in enumerate(samples):
                document = {
                    'model': model_name,
                    'doc_id': f"{profile_id}_{i}",
                    'profile_id': profile_id,
                    'age_class': age_class,
                    'text': s,
                    'instruction': instruction
                }
                for k, v in role.items():
                    document[k] = v
                collection.append(document)

            if counter >= buffer:
                db.insert_many(collection)
                collection = []
                counter = 0
