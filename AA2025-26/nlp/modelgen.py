from model_text_gen import LocalInstructGenerator
from openai_text_gen import OpenAIInstructGenerator
import openai_text_gen as opn
import model_text_gen as mtg
import torch 
import json 
from tqdm import tqdm 

with open("./data/profiles.json", 'r') as infile:
    jprofile = json.load(infile)

profiles = jprofile['profiles']

open_model_name = "mistralai/Mistral-7B-Instruct-v0.3"
# "meta-llama/Meta-Llama-3.1-8B-Instruct"
closed_model_name = "gpt-4o-mini"

open_model = True

if __name__ == "__main__":

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

    collection = []


    system_prompt = (
        "Agisci come una persona reale italiana. Rispetta rigorosamente il ruolo e lo stile indicati. "
    )
    instruction = "Scrivi un breve testo sulle cose importanti della vita"

    for profile in tqdm(profiles[:10]):

        metadata = profile['metadata']
        profile_id = metadata['id']
        age_class = metadata['age_class']
        role = profile['data']

        samples = gen.generate_role_texts(
            role=role,
            instruction=instruction,
            n_samples=10
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

    with open(f"./data/life/corpus_{model_name.split('/')[-1]}.json", "w") as out:
        json.dump({'docs': collection}, out)
