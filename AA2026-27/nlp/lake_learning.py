from collections import defaultdict

import matplotlib.pyplot as plt

from nlp.lake_agent import ACTIONS, NAMES, PLAYING, REACHED, Lake
from nlp.lake_learning_rules import (
    features, reward, choose_epsilon_greedy, choose_greedy, learn_q,
)


class LearningAgent:
    """An agent whose behaviour is made of four functions and a table.

    features: situation -> state
    choose:   (values, state) -> action
    learn:    updates `values` after each move
    reward:   status -> number

    The functions live in `nlp/lake_learning_rules.py`. The agent is called
    like a hand-written rule: agent(view, visits, compass) returns an action.
    """

    def __init__(self, features=features, choose=choose_epsilon_greedy, learn=learn_q, reward=reward):
        self.features = features
        self.choose = choose
        self.learn = learn
        self.reward = reward
        self.values = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def __call__(self, view, visits, compass):
        return self.choose(self.values, self.features(view, visits, compass))


def observe(lake):
    return lake.look(), lake.notebook(), lake.compass()


def train(agent, episodes=2000, lake=None, max_moves=None):
    """Let the agent play and learn. Returns the outcome of each episode."""
    lake = lake or Lake()
    if max_moves is not None:
        lake.max_moves = max_moves
    outcomes = []
    for _ in range(episodes):
        lake.reset()
        while lake.status == PLAYING:
            state = agent.features(*observe(lake))
            action = agent(*observe(lake))
            lake.step(action)
            next_state = agent.features(*observe(lake))
            agent.learn(agent.values, state, action, agent.reward(lake.status),
                        next_state, lake.status != PLAYING)
        outcomes.append(lake.status)
    return outcomes


def greedy(agent):
    """The same agent, without exploring: it only uses what it has learned."""
    def choose(view, visits, compass):
        return choose_greedy(agent.values, agent.features(view, visits, compass))
    return choose


def plot_learning(outcomes, window=100):
    """Share of episodes ending at the goal, in consecutive blocks."""
    blocks = range(0, len(outcomes) - window + 1, window)
    shares = [sum(o == REACHED for o in outcomes[i:i + window]) / window for i in blocks]
    plt.figure(figsize=(6, 3))
    plt.plot([i + window for i in blocks], shares)
    plt.ylim(0, 1.05)
    plt.xlabel("partite giocate")
    plt.ylabel("traguardo raggiunto")
    plt.show()


def show_values(agent, limit=10):
    """Print the learned values for the states with the largest preferences."""
    rows = sorted(agent.values.items(), key=lambda kv: -max(kv[1].values()))[:limit]
    for state, values in rows:
        view, compass = state[0], state[1]
        cells = ", ".join(f"{NAMES[a]}={c}" for a, c in zip(ACTIONS, view))
        learned = ", ".join(f"{NAMES[a]}: {v:+.2f}" for a, v in values.items())
        print(f"vede [{cells}] bussola {compass}\n    -> {learned}")
