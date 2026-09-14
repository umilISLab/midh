import random
import statistics


def binary_guess(low: int, high: int) -> int:
    return (low + high) // 2


def random_guess(low: int, high: int) -> int:
    return random.randint(low, high)


def linear_guess(low: int, high: int) -> int:
    return low


def fixed_split_guess(fraction: float):
    def guess(low: int, high: int) -> int:
        point = low + round(fraction * (high - low))
        return max(low, min(high - 1, point))

    return guess


STRATEGIES = {
    "bisezione": binary_guess,
    "casuale": random_guess,
    "lineare": linear_guess,
}


def play(secret: int, low: int, high: int, choose_guess) -> int:
    questions_asked = 0
    while low < high:
        guess = choose_guess(low, high)
        questions_asked += 1
        if secret > guess:
            low = guess + 1
        else:
            high = guess
    return questions_asked


def compare_strategies(strategies: dict = STRATEGIES, low: int = 1, high: int = 100, repetitions: int = 20) -> dict:
    results = {}
    for name, strategy in strategies.items():
        counts = [
            play(secret, low, high, strategy)
            for secret in range(low, high + 1)
            for _ in range(repetitions)
        ]
        results[name] = counts
    return results


def print_comparison(results: dict) -> None:
    print(f"{'strategia':<15}{'media':>10}{'minimo':>10}{'massimo':>10}")
    for name, counts in results.items():
        print(f"{name:<15}{statistics.mean(counts):>10.2f}{min(counts):>10}{max(counts):>10}")


def print_examples(strategies: dict, secrets: list, low: int, high: int) -> None:
    header = f"{'numero segreto':<16}" + "".join(f"{name:>15}" for name in strategies)
    print(header)
    for secret in secrets:
        row = f"{secret:<16}"
        for strategy in strategies.values():
            row += f"{play(secret, low, high, strategy):>15}"
        print(row)
