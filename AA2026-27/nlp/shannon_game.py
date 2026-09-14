import random

WORDS = [
    "biblioteca",
    "manoscritto",
    "letteratura",
    "linguaggio",
    "vocabolario",
    "montagna",
    "finestra",
    "avventura",
    "temperatura",
    "particolare",
]


def play_shannon_game(word: str = None, max_attempts: int = 30) -> None:
    if word is None:
        word = random.choice(WORDS)

    word = word.lower()

    print("Indovina, una lettera alla volta, la parola che ho in mente.")
    print(f"E' lunga {len(word)} lettere: \"{format_placeholder(word, 0)}\"")
    print(f"Hai al massimo {max_attempts} tentativi per ogni lettera. Scrivi 'quit' per arrenderti.")

    results = []

    for position in range(len(word)):
        character = word[position]
        print(f"\nParola finora: \"{format_placeholder(word, position)}\"")
        attempts = 0
        guessed = False

        while attempts < max_attempts:
            raw_guess = input("Prossima lettera? ").lower()
            guess = raw_guess.strip()

            if guess == "quit":
                print(f"\nGioco interrotto. La parola era: \"{word}\"")
                print_position_statistics(results, word)
                return

            if len(guess) != 1:
                print("Scrivi una sola lettera.")
                continue

            attempts += 1

            if guess == character:
                guessed = True
                break

            if attempts < max_attempts:
                print("Non è quella. Riprova.")

        if guessed:
            print(f"Esatto! Tentativi: {attempts}")
        else:
            print(f"Tentativi esauriti. Era: \"{character}\"")

        results.append(attempts if guessed else None)

    print(f"\nLa parola completa era: \"{word}\"")
    print_position_statistics(results, word)


def format_placeholder(word: str, revealed_up_to: int) -> str:
    characters = list(word[:revealed_up_to]) + ["_"] * (len(word) - revealed_up_to)
    return " ".join(characters)


def print_position_statistics(results: list, word: str) -> None:
    print("\nRiepilogo per posizione:")
    print(f"{'posizione':<12}{'lettera':<10}{'tentativi':>10}")
    for position, attempts in enumerate(results):
        attempts_label = attempts if attempts is not None else "-"
        print(f"{position + 1:<12}{word[position]:<10}{attempts_label:>10}")
