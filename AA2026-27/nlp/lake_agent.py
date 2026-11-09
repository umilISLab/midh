import time
from collections import Counter

import matplotlib.pyplot as plt
from IPython.display import clear_output

UP, RIGHT, LEFT, DOWN = 0, 1, 2, 3
ACTIONS = [UP, RIGHT, LEFT, DOWN]
MOVES = {UP: (0, -1), RIGHT: (1, 0), LEFT: (-1, 0), DOWN: (0, 1)}
NAMES = {UP: "UP", RIGHT: "RIGHT", LEFT: "LEFT", DOWN: "DOWN"}

FREE, HOLE, WALL, GOAL = "free", "hole", "wall", "goal"
PLAYING, FELL, REACHED, TIMEOUT = "playing", "fell", "reached", "timeout"

HOLES = [(1, 1), (3, 1), (4, 2), (0, 3), (2, 3)]

MESSAGES = {
    PLAYING: "",
    FELL: "Sei caduto in un buco!",
    REACHED: "Traguardo raggiunto!",
    TIMEOUT: "Mosse finite.",
}


def sign(value):
    return (value > 0) - (value < 0)


class Lake:
    """The world: a grid with holes, a start and a goal.

    Coordinates are (x, y): x is the column, y is the row, the origin is
    the top-left corner. The agent never sees the grid, only what `look`,
    `notebook` and `compass` report.
    """

    def __init__(self, width=5, height=5, holes=HOLES, start=(0, 0), goal=None, max_moves=None):
        self.width = width
        self.height = height
        self.holes = list(holes)
        self.start = start
        self.goal = goal if goal is not None else (width - 1, height - 1)
        self.max_moves = max_moves if max_moves is not None else 4 * width * height
        self.reset()

    def reset(self):
        self.position = self.start
        self.visits = {self.start: 1}
        self.moves = 0
        self.status = PLAYING

    def cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return WALL
        if (x, y) in self.holes:
            return HOLE
        if (x, y) == self.goal:
            return GOAL
        return FREE

    def neighbour(self, action):
        dx, dy = MOVES[action]
        return self.position[0] + dx, self.position[1] + dy

    def look(self):
        return {action: self.cell(*self.neighbour(action)) for action in ACTIONS}

    def notebook(self):
        return {action: self.visits.get(self.neighbour(action), 0) for action in ACTIONS}

    def compass(self):
        return sign(self.goal[0] - self.position[0]), sign(self.goal[1] - self.position[1])

    def step(self, action):
        if action not in ACTIONS:
            raise ValueError(f"Azione non valida: {action!r}. Usa UP, RIGHT, LEFT o DOWN.")
        target = self.neighbour(action)
        if self.cell(*target) != WALL:
            self.position = target
        self.moves += 1
        self.visits[self.position] = self.visits.get(self.position, 0) + 1
        if self.position in self.holes:
            self.status = FELL
        elif self.position == self.goal:
            self.status = REACHED
        elif self.moves >= self.max_moves:
            self.status = TIMEOUT


def draw(lake, size=4.5, title=""):
    plt.figure(figsize=(size, size))

    for x in range(lake.width + 1):
        plt.plot([x, x], [0, lake.height], color="gray", linewidth=0.5)
    for y in range(lake.height + 1):
        plt.plot([0, lake.width], [y, y], color="gray", linewidth=0.5)

    for (x, y), count in lake.visits.items():
        plt.text(x + 0.08, y + 0.2, str(count), fontsize=8, color="gray")

    for x, y in lake.holes:
        plt.scatter(x + 0.5, y + 0.5, marker="o", s=200, color="black")
    plt.scatter(lake.goal[0] + 0.5, lake.goal[1] + 0.5, marker="s", s=200, color="green")
    plt.scatter(lake.position[0] + 0.5, lake.position[1] + 0.5, marker="^", s=200, color="red")

    plt.xlim(-0.05, lake.width + 0.05)
    plt.ylim(lake.height + 0.05, -0.05)
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.title(title)


def episode(agent, lake, on_step=None):
    lake.reset()
    if on_step:
        on_step(lake)
    while lake.status == PLAYING:
        lake.step(agent(lake.look(), lake.notebook(), lake.compass()))
        if on_step:
            on_step(lake)
    return lake.status


def describe(values):
    return "{" + ", ".join(f"{NAMES[action]}: {value!r}" for action, value in values.items()) + "}"


def run(agent, lake=None, delay=0.2, show_inputs=False, max_moves=None):
    lake = lake or Lake()
    if max_moves is not None:
        lake.max_moves = max_moves
    received = []

    def spy(view, visits, compass):
        action = agent(view, visits, compass)
        received[:] = [view, visits, compass, action]
        return action

    def show(current):
        clear_output(wait=True)
        message = MESSAGES[current.status]
        draw(current, title=f"Mossa {current.moves}  {message}".strip())
        plt.show()
        if show_inputs and received:
            view, visits, compass, action = received
            print("Per decidere questa mossa choose_action ha ricevuto:")
            print(f"view    = {describe(view)}")
            print(f"visits  = {describe(visits)}")
            print(f"compass = {compass}")
            print(f"scelta  = {NAMES[action]}")
        time.sleep(delay)

    episode(spy, lake, on_step=show)


def evaluate(agent, episodes=100, lake=None, max_moves=None):
    lake = lake or Lake()
    if max_moves is not None:
        lake.max_moves = max_moves
    outcomes = Counter(episode(agent, lake) for _ in range(episodes))
    return {status: outcomes[status] / episodes for status in (REACHED, FELL, TIMEOUT)}
