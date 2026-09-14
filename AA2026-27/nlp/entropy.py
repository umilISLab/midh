import collections
import math
import random


def equiprobable_entropy(n: int) -> float:
    return math.log2(n)


def normalize_text(text: str) -> str:
    characters = [character for character in text.lower() if character.isalpha() or character.isspace()]
    normalized = "".join(" " if character.isspace() else character for character in characters)
    return " ".join(normalized.split())


def letter_frequencies(text: str) -> dict:
    counts = collections.Counter(text)
    total = len(text)
    return {character: count / total for character, count in counts.items()}


def entropy(frequencies: dict) -> float:
    return -sum(p * math.log2(p) for p in frequencies.values() if p > 0)


def random_text(length: int, alphabet: str) -> str:
    return "".join(random.choices(alphabet, k=length))
