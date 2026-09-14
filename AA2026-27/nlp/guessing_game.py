import math


def play_guess_the_number(low: int = 1, high: int = 100) -> None:
    print(f"Pensa un numero tra {low} e {high}. Rispondi 'si' o 'no' alle mie domande (o 'quit' per interrompere).")
    range_size = high - low + 1
    questions_asked = 0

    while low < high:
        mid = (low + high) // 2
        answer = input(f"E' maggiore di {mid}? (si/no) ").strip().lower()

        if answer == "quit":
            print("Gioco interrotto.")
            return

        questions_asked += 1

        if answer in ("si", "s", "yes", "y"):
            low = mid + 1
        elif answer in ("no", "n"):
            high = mid
        else:
            print("Rispondi con 'si' o 'no'.")
            questions_asked -= 1

    print(f"Il tuo numero è {low}!")
    print(f"Domande necessarie: {questions_asked}")
    print(f"Numero minimo di domande possibile: {math.ceil(math.log2(range_size))}")
