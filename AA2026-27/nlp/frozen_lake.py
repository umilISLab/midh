import random

from IPython.display import clear_output

MAP = ["SFFF", "FHFH", "FFFH", "HFFG"]

SYMBOLS = {"S": "🟩", "F": "🟦", "H": "⬛", "G": "🏁"}

ACTIONS = ["a", "s", "d", "w"]

MOVES = {"a": (0, -1), "s": (1, 0), "d": (0, 1), "w": (-1, 0)}

HELP = "Muovi con w (su), a (sinistra), s (giù), d (destra); q per uscire."


def render(row: int, col: int, symbol: str = "🧍") -> str:
    lines = []
    for r, line in enumerate(MAP):
        cells = [symbol if (r, c) == (row, col) else SYMBOLS[cell] for c, cell in enumerate(line)]
        lines.append("".join(cells))
    return "\n".join(lines)


def play(slippery: bool = False) -> None:
    row, col, steps = 0, 0, 0
    message = HELP
    while True:
        clear_output(wait=True)
        print(render(row, col))
        print(f"\nMosse: {steps}")
        print(message)
        key = input("Mossa: ").strip().lower()
        if key == "q":
            print("Partita interrotta.")
            return
        if key not in MOVES:
            message = "Mossa non valida. " + HELP
            continue
        message = HELP
        if slippery:
            slipped = ACTIONS[(ACTIONS.index(key) + random.choice([-1, 0, 1])) % 4]
            if slipped != key:
                message = "Il ghiaccio ti ha fatto scivolare! " + HELP
            key = slipped
        d_row, d_col = MOVES[key]
        row = min(max(row + d_row, 0), len(MAP) - 1)
        col = min(max(col + d_col, 0), len(MAP[0]) - 1)
        steps += 1
        if MAP[row][col] == "H":
            clear_output(wait=True)
            print(render(row, col, "💀"))
            print(f"\nSei caduto nel lago dopo {steps} mosse.")
            return
        if MAP[row][col] == "G":
            clear_output(wait=True)
            print(render(row, col, "🎉"))
            print(f"\nHai raggiunto il traguardo in {steps} mosse!")
            return
