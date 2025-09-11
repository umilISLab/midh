import numpy as np 


def odds_to_probability(odds: float):
    """
    Nel sistema europeo di quote, la quota si
    ottiene come 1 / probabilità
    Per ottenere la probabilità dobbiamo perciò
    dividere 1 per la quota
    """
    return 1 / odds 

def entropy(probabilities: np.ndarray):
    h = 0
    for p in probabilities:
        h += p * np.log2(p)
    return -h