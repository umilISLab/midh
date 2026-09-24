import math
import time
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from IPython.display import clear_output

COLORS = {
    "nero": "black", "rosso": "red", "blu": "blue", "verde": "green",
    "giallo": "gold", "arancione": "orange", "viola": "purple",
    "rosa": "hotpink", "marrone": "saddlebrown", "grigio": "gray",
}

ARGUMENTS = {
    "avanti": 1, "indietro": 1, "destra": 1, "sinistra": 1,
    "alza": 0, "abbassa": 0, "colore": 1, "spessore": 1, "ripeti": 1,
}


class ToyLanguageError(Exception):
    pass


@dataclass
class Turtle:
    x: float = 0.0
    y: float = 0.0
    heading: float = 90.0
    pen_down: bool = True
    color: str = "black"
    width: float = 2.0
    segments: list = field(default_factory=list)

    def move(self, distance: float) -> None:
        new_x = self.x + distance * math.cos(math.radians(self.heading))
        new_y = self.y + distance * math.sin(math.radians(self.heading))
        if self.pen_down:
            self.segments.append((self.x, self.y, new_x, new_y, self.color, self.width))
        self.x, self.y = new_x, new_y


def tokenize(source: str) -> list:
    lines = [line.split("#")[0] for line in source.splitlines()]
    text = " ".join(lines).replace("[", " [ ").replace("]", " ] ")
    return text.split()


def parse(tokens: list) -> list:
    program, position = _parse_block(tokens, 0, nested=False)
    return program


def _parse_block(tokens: list, position: int, nested: bool):
    block = []
    while position < len(tokens):
        token = tokens[position]
        if token == "]":
            if not nested:
                raise ToyLanguageError("']' senza '[' corrispondente")
            return block, position + 1
        if token == "[":
            raise ToyLanguageError("'[' inatteso: le parentesi quadre seguono solo 'ripeti N'")
        if token not in ARGUMENTS:
            raise ToyLanguageError(f"comando sconosciuto: '{token}'")
        position += 1
        args = []
        for _ in range(ARGUMENTS[token]):
            if position >= len(tokens) or tokens[position] in ("[", "]"):
                raise ToyLanguageError(f"'{token}' richiede un argomento")
            args.append(tokens[position])
            position += 1
        if token == "ripeti":
            if position >= len(tokens) or tokens[position] != "[":
                raise ToyLanguageError("'ripeti N' deve essere seguito da '[ ... ]'")
            body, position = _parse_block(tokens, position + 1, nested=True)
            block.append(("ripeti", _number(token, args[0]), body))
        elif token == "colore":
            if args[0] not in COLORS:
                raise ToyLanguageError(f"colore sconosciuto: '{args[0]}'")
            block.append((token, COLORS[args[0]]))
        elif token in ("alza", "abbassa"):
            block.append((token,))
        else:
            block.append((token, _number(token, args[0])))
    if nested:
        raise ToyLanguageError("manca un ']' di chiusura")
    return block, position


def _number(command: str, text: str) -> float:
    try:
        return float(text)
    except ValueError:
        raise ToyLanguageError(f"'{command}' richiede un numero, non '{text}'")


def execute(program: list, turtle: Turtle = None) -> Turtle:
    turtle = turtle or Turtle()
    for instruction in program:
        name = instruction[0]
        if name == "avanti":
            turtle.move(instruction[1])
        elif name == "indietro":
            turtle.move(-instruction[1])
        elif name == "destra":
            turtle.heading -= instruction[1]
        elif name == "sinistra":
            turtle.heading += instruction[1]
        elif name == "alza":
            turtle.pen_down = False
        elif name == "abbassa":
            turtle.pen_down = True
        elif name == "colore":
            turtle.color = instruction[1]
        elif name == "spessore":
            turtle.width = instruction[1]
        elif name == "ripeti":
            for _ in range(int(instruction[1])):
                execute(instruction[2], turtle)
    return turtle


def run(source: str) -> Turtle:
    return execute(parse(tokenize(source)))


def flatten(program: list) -> list:
    steps = []
    for instruction in program:
        if instruction[0] == "ripeti":
            for _ in range(int(instruction[1])):
                steps.extend(flatten(instruction[2]))
        else:
            steps.append(instruction)
    return steps


def bounds(turtle: Turtle, margin: float = 0.1):
    xs = [0.0, turtle.x] + [v for s in turtle.segments for v in (s[0], s[2])]
    ys = [0.0, turtle.y] + [v for s in turtle.segments for v in (s[1], s[3])]
    half = max(max(xs) - min(xs), max(ys) - min(ys), 1.0) / 2 * (1 + margin)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return (cx - half, cx + half), (cy - half, cy + half)


def draw(turtle: Turtle, ax=None, size: float = 4.0, limits=None, title: str = None):
    if ax is None:
        _, ax = plt.subplots(figsize=(size, size))
    for x0, y0, x1, y1, color, width in turtle.segments:
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=width, solid_capstyle="round")
    ax.plot(
        turtle.x, turtle.y, marker=(3, 0, turtle.heading - 90),
        color="seagreen", markersize=12,
    )
    ax.set_aspect("equal")
    if limits:
        ax.set_xlim(limits[0])
        ax.set_ylim(limits[1])
    if title:
        ax.set_title(title, fontfamily="monospace")
    ax.axis("off")
    return ax


def show(source: str, ax=None, size: float = 4.0):
    try:
        turtle = run(source)
    except ToyLanguageError as error:
        print(f"Errore: {error}")
        return None
    draw(turtle, ax, size)
    return turtle


def animate(source: str, delay: float = 0.5, size: float = 4.0):
    try:
        program = parse(tokenize(source))
    except ToyLanguageError as error:
        print(f"Errore: {error}")
        return None
    steps = flatten(program)
    limits = bounds(execute(program))
    turtle = Turtle()
    for instruction in [None] + steps:
        if instruction is not None:
            execute([instruction], turtle)
        clear_output(wait=True)
        label = " ".join(str(part) for part in instruction) if instruction else "start"
        draw(turtle, size=size, limits=limits, title=label)
        plt.show()
        time.sleep(delay)
    return turtle
