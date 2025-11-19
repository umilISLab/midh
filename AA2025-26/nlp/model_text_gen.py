import os
import torch
import random
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextIteratorStreamer,
    set_seed,
)

@dataclass
class GenConfig:
    model_id: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"  # good multilingual Italian
    device_map: Union[str, Dict] = "auto"
    dtype: Optional[torch.dtype] = torch.float16  # None -> model default
    load_in_4bit: bool = False  # requires bitsandbytes
    max_new_tokens: int = 140
    temperature: float = 0.8
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.05
    seed: Optional[int] = 42
    # Stop sequences: include Italian line breaks or explicit tags if you use them
    stop_sequences: Optional[List[str]] = None  # e.g., ["</s>", "###"]

class LocalInstructGenerator:
    """
    Lightweight wrapper around HF Transformers for local instruction-tuned models.
    Works with chat-template models (Llama/Mistral) and plain instruct models.
    """

    def __init__(self, cfg: GenConfig):
        self.cfg = cfg
        if cfg.seed is not None:
            set_seed(cfg.seed)
            random.seed(cfg.seed); np.random.seed(cfg.seed)

        load_kwargs = dict(
            device_map=cfg.device_map,
        )
        if cfg.load_in_4bit:
            load_kwargs.update(dict(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            ))
        elif cfg.dtype is not None:
            load_kwargs.update(dict(torch_dtype=cfg.dtype))

        self.tokenizer = AutoTokenizer.from_pretrained(cfg.model_id, use_fast=True)
        # Ensure we have an EOS token for stopping
        if self.tokenizer.eos_token_id is None and self.tokenizer.sep_token_id is not None:
            self.tokenizer.eos_token_id = self.tokenizer.sep_token_id

        self.model = AutoModelForCausalLM.from_pretrained(cfg.model_id, **load_kwargs)
        self.model.eval()

        # Detect if model has a chat template
        self._has_chat_template = hasattr(self.tokenizer, "apply_chat_template") and \
                                  (self.tokenizer.chat_template is not None)

    def _build_chat_messages(
        self,
        system: str,
        user: str
    ) -> List[Dict[str, str]]:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        return messages

    def _encode(
        self,
        system_prompt: str,
        user_prompt: str
    ):
        """
        Builds the right input format for chat models (Llama/Mistral) or plain models.
        """
        if self._has_chat_template:
            messages = self._build_chat_messages(system_prompt, user_prompt)
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            inputs = self.tokenizer(text, return_tensors="pt")
        else:
            # Fallback: simple instruct format
            prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:"
            inputs = self.tokenizer(prompt, return_tensors="pt")
        return {k: v.to(self.model.device) for k, v in inputs.items()}

    @torch.inference_mode()
    def generate_once(
        self,
        system_prompt: str,
        user_prompt: str,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """
        Single text generation call.
        """
        if seed is not None:
            set_seed(seed); random.seed(seed); np.random.seed(seed)

        cfg = self.cfg
        stop_sequences = stop_sequences or cfg.stop_sequences or []

        inputs = self._encode(system_prompt, user_prompt)

        gen_out = self.model.generate(
            **inputs,
            do_sample=True,
            max_new_tokens=max_new_tokens or cfg.max_new_tokens,
            temperature=temperature if temperature is not None else cfg.temperature,
            top_p=top_p if top_p is not None else cfg.top_p,
            top_k=top_k if top_k is not None else cfg.top_k,
            repetition_penalty=repetition_penalty if repetition_penalty is not None else cfg.repetition_penalty,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        decoded = self.tokenizer.decode(gen_out[0], skip_special_tokens=True)

        # If chat-template, the decoded contains the whole conversation; extract the assistant tail
        if self._has_chat_template:
            # naive postcut: find last occurrence of user prompt and take the tail
            tail = decoded.rsplit(user_prompt, 1)[-1]
            text = tail.strip()
        else:
            # remove the leading prompt up to "Assistant:"
            split_tok = "Assistant:"
            text = decoded.split(split_tok, 1)[-1].strip()

        # Apply custom stop sequences
        for stop in stop_sequences:
            idx = text.find(stop)
            if idx != -1:
                text = text[:idx].strip()
                break
        return text

    def generate_role_texts(
        self,
        role: Dict[str, Union[str, int]],
        instruction: str,
        n_samples: int = 5,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Tuple[str] = None,
        **gen_kwargs
    ) -> List[str]:
        """
        Generate short Italian texts by impersonating a role.

        role: e.g. {"profession": "insegnante di scuola primaria", "age": 42, "city": "Bologna", "tone": "colloquiale"}
        instruction: the concrete task (in Italian), e.g. "Scrivi un breve testo (3-5 frasi) sul valore della lettura."
        """
        # Build an Italian system prompt that anchors persona and output style
        # Keep it compact and directive to help adherence.
        persona_lines = []
        for k, v in role.items():
            persona_lines.append(f"- {k}: {v}")
        persona_block = "\n".join(persona_lines)

        if system_prompt is None:
            system_prompt = (
                "Agisci come una persona reale italiana. Rispetta rigorosamente il ruolo e lo stile indicati. "
                "Usa italiano naturale, frasi brevi, e mantieni la coerenza della voce. "
                "Evita anglicismi gratuiti e formule ripetitive."
            )

        user_prompt = (
            "Ruolo:\n"
            f"{persona_block}\n\n"
            "Istruzione:\n"
            f"{instruction}\n\n"
            "Vincoli:\n"
            "- Lunghezza: 3–6 frasi.\n"
            "- Niente elenco puntato; usa prosa naturale.\n"
            "- Evita disclaimer sul fatto che sei un'IA.\n"
        )

        outputs = []
        for i in range(n_samples):
            # small per-sample seed jitter for variety while remaining reproducible overall
            seed_i = (self.cfg.seed or 0) + i if self.cfg.seed is not None else None
            txt = self.generate_once(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                seed=seed_i,
                **gen_kwargs
            )
            outputs.append(txt)
        return outputs


