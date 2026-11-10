"""Minimum Number of Pushes to Type Word II at length 10^5 with skewed letter frequencies."""

from string import ascii_lowercase

SEEDS = 2
N = 10**5


def generate(rng):
    weights = [rng.random() ** 3 for _ in ascii_lowercase]
    return {"word": "".join(rng.choices(ascii_lowercase, weights=weights, k=N))}
