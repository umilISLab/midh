import random

from nlp.lake_agent import UP, RIGHT, LEFT, DOWN, ACTIONS, REACHED, FELL

EPSILON = 0.2  # how often the agent tries a random move
ALPHA = 0.5    # how much a new experience weighs
GAMMA = 0.9    # how much future reward counts


def features(view, visits, compass):
    """Reduce what the agent perceives to the state it learns about.

    view:    what is in the four adjacent cells (FREE, HOLE, WALL, GOAL)
    visits:  how many times I have been in each adjacent cell
    compass: where the goal is, as (dx, dy) with values -1, 0 or 1

    Two situations with the same features are, for the agent, the same
    situation. Returns something that can be a dictionary key (a tuple).
    """
    return (tuple(view[a] for a in ACTIONS), compass)


def features_with_notebook(view, visits, compass):
    """Like `features`, but also remembers which adjacent cells it has visited."""
    return (tuple(view[a] for a in ACTIONS), compass, tuple(min(visits[a], 1) for a in ACTIONS))


def reward(status):
    """The reward the lake gives after a move, from the status it ends in.

    status: PLAYING, REACHED, FELL or TIMEOUT

    Returns a number: positive is good, negative is bad.
    """
    if status == REACHED:
        return 1.0
    if status == FELL:
        return -1.0
    return -0.01


def choose_greedy(values, state):
    """Pick the action with the highest learned value.

    values: the table, values[state][action] is a number (0 if never tried)
    state:  the result of `features`

    Returns one of UP, RIGHT, LEFT, DOWN. Ties are broken at random.
    """
    best = max(values[state].values())
    return random.choice([a for a, v in values[state].items() if v == best])


def choose_epsilon_greedy(values, state):
    """Usually the best known action, sometimes a random one (to explore)."""
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    return choose_greedy(values, state)


def choose_random(values, state):
    """Ignore what has been learned."""
    return random.choice(ACTIONS)


def learn_q(values, state, action, reward, next_state, finished):
    """Update the table after one move (Q-learning).

    values:     the table, values[state][action] is a number
    state:      the situation before the move
    action:     the move that was made
    reward:     what the lake gave back
    next_state: the situation after the move
    finished:   True if the partita ended with this move

    The function changes `values` in place and returns nothing.
    """
    future = 0.0 if finished else max(values[next_state].values())
    old = values[state][action]
    values[state][action] = old + ALPHA * (reward + GAMMA * future - old)


def learn_immediate(values, state, action, reward, next_state, finished):
    """Learn only from the reward of the move, ignoring what comes next."""
    old = values[state][action]
    values[state][action] = old + ALPHA * (reward - old)
