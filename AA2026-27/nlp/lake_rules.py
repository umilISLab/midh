import random

from nlp.lake_agent import UP, RIGHT, LEFT, DOWN, FREE, HOLE, WALL, GOAL


def choose_action_go_right(view, visits, compass):
    """Decide the next move from what the agent sees and remembers.

    view:    what is in the four adjacent cells,
             e.g. view[RIGHT] is FREE, HOLE, WALL or GOAL
    visits:  how many times I have been in each adjacent cell,
             e.g. visits[UP] == 0 means I have never been there
    compass: where the goal is, as (dx, dy) with values -1, 0 or 1;
             dx == 1 means to the right, dy == 1 means below

    Returns one of UP, RIGHT, LEFT, DOWN.
    """
    return RIGHT

def choose_action_random(view, visits, compass):
    """Decide the next move from what the agent sees and remembers.

    view:    what is in the four adjacent cells,
             e.g. view[RIGHT] is FREE, HOLE, WALL or GOAL
    visits:  how many times I have been in each adjacent cell,
             e.g. visits[UP] == 0 means I have never been there
    compass: where the goal is, as (dx, dy) with values -1, 0 or 1;
             dx == 1 means to the right, dy == 1 means below

    Returns one of UP, RIGHT, LEFT, DOWN.
    """
    action = random.choice([UP, DOWN, RIGHT, LEFT])
    return action

def choose_action_free_view(view, visits, compass):
    """Decide the next move from what the agent sees and remembers.

    view:    what is in the four adjacent cells,
             e.g. view[RIGHT] is FREE, HOLE, WALL or GOAL
    visits:  how many times I have been in each adjacent cell,
             e.g. visits[UP] == 0 means I have never been there
    compass: where the goal is, as (dx, dy) with values -1, 0 or 1;
             dx == 1 means to the right, dy == 1 means below

    Returns one of UP, RIGHT, LEFT, DOWN.
    """
    preferences = []
    for k, v in view.items():
        if v in [FREE, GOAL]:
            preferences.append(k)
            if v == GOAL:
                preferences = [k]
                break
    if len(preferences) > 0:
        action = random.choice(preferences)
    else:
        action = random.choice([UP, DOWN, LEFT, RIGHT])
    return action

def choose_action_free_memory(view, visits, compass):
    """Decide the next move from what the agent sees and remembers.

    view:    what is in the four adjacent cells,
             e.g. view[RIGHT] is FREE, HOLE, WALL or GOAL
    visits:  how many times I have been in each adjacent cell,
             e.g. visits[UP] == 0 means I have never been there
    compass: where the goal is, as (dx, dy) with values -1, 0 or 1;
             dx == 1 means to the right, dy == 1 means below

    Returns one of UP, RIGHT, LEFT, DOWN.
    """
    preferences = []
    for k, v in view.items():
        if v in [FREE, GOAL]:
            preferences.append((k, visits[k]))
            if v == GOAL:
                preferences = [(k, 0)]
                break
    best_action, best_count = UP, 10000
    if len(preferences) > 0:
        for direction, count in preferences:
            if count < best_count:
                best_count = count
                best_action = direction
        action = best_action
    else:
        action = random.choice([UP, DOWN, LEFT, RIGHT])
    return action
