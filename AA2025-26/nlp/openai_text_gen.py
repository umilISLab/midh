import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from openai import OpenAI

@dataclass
class GenConfig:
    # OpenAI model id; pick a fast, low-cost model for generation at scale
    model: str = "gpt-4o-mini"
    max_new_tokens: int = 140            # aka max_tokens in Chat Completions
    temperature: float = 0.9
    top_p: float = 0.92
    top_k: Optional[int] = None          # not supported in Chat Completions; kept for API symmetry
    repetition_penalty: Optional[float] = None  # not supported; kept for symmetry
    # Note: deterministic seeding is not guaranteed; parameter may be ignored by the service.
    seed: Optional[int] = None
    # You can pass a custom system message if you want to override the default below
    system_prefix_it: str = (
        "Agisci come una persona reale italiana. Rispetta rigorosamente il ruolo e lo stile indicati. "
        "Usa italiano naturale, frasi brevi, e mantieni la coerenza della voce. "
        "Evita anglicismi gratuiti e formule ripetitive."
    )

class OpenAIInstructGenerator:
    """
    Drop-in replacement for the local generator, but backed by the OpenAI Chat Completions API.
    Mirrors the same public methods:
      - generate_once(system_prompt, user_prompt, ...)
      - generate_role_texts(role, instruction, n_samples, ...)
    """
    def __init__(self, cfg: GenConfig, api_key: Optional[str] = None):
        self.cfg = cfg
        # The OpenAI client picks up OPENAI_API_KEY from env if not provided
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        self.client = OpenAI()

    def _messages(self, system_prompt: str, user_prompt: str):
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def generate_once(
        self,
        system_prompt: str,
        user_prompt: str,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        seed: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Single generation call via Chat Completions.
        Notes:
          - top_k and repetition_penalty are not supported by this endpoint.
          - 'seed' may be ignored; determinism is not guaranteed.
        """
        cfg = self.cfg
        params = dict(
            model=cfg.model,
            messages=self._messages(system_prompt, user_prompt),
            max_tokens=max_new_tokens or cfg.max_new_tokens,
            temperature=cfg.temperature if temperature is None else temperature,
            top_p=cfg.top_p if top_p is None else top_p,
        )
        # Pass-through seed if provided (some models/endpoints accept it; safe to include)
        if seed is not None or cfg.seed is not None:
            params["seed"] = seed if seed is not None else cfg.seed

        resp = self.client.chat.completions.create(**params)
        return (resp.choices[0].message.content or "").strip()

    def generate_role_texts(
        self,
        role: Dict[str, str],
        instruction: str,
        n_samples: int = 5,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **gen_kwargs,
    ) -> List[str]:
        """
        Generate short Italian texts by impersonating a role.
        role example:
            {"profession": "insegnante di scuola primaria", "age": "42", "city": "Bologna", "tone": "colloquiale"}
        instruction example:
            "Scrivi un breve testo (3-6 frasi) sul valore della lettura."
        """
        persona_lines = [f"- {k}: {v}" for k, v in role.items()]
        persona_block = "\n".join(persona_lines)

        system_prompt = self.cfg.system_prefix_it
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

        out = []
        for i in range(n_samples):
            # small per-sample seed jitter if a base seed is set
            seed_i = (self.cfg.seed + i) if (self.cfg.seed is not None) else None
            txt = self.generate_once(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                seed=seed_i,
                **gen_kwargs,
            )
            out.append(txt)
        return out


