"""Minimum Number of Pushes to Type Word II at length 10^5 with skewed letter frequencies."""

SEEDS = 2
N = 10**5
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    weights = [rng.random() ** 3 for _ in LETTERS]
    return {"word": "".join(rng.choices(LETTERS, weights=weights, k=N))}
