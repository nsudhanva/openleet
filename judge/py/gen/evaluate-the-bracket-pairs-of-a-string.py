"""Evaluate the Bracket Pairs of a String with 10^5 distinct 4-letter keys and ~14,000 pairs
whose keys sit in the last tenth of the knowledge list (or are unknown), so a linear search of
the list per pair does ~10^9 comparisons."""

from itertools import islice, product
from string import ascii_lowercase

SEEDS = 3
K = 100_000
TAIL = 10_000
PAIRS = 14_000
UNKNOWN = 0.2


def generate(rng):
    keys = ["".join(p) for p in islice(product(ascii_lowercase, repeat=4), K)]
    rng.shuffle(keys)
    values = ["".join(rng.choices(ascii_lowercase, k=rng.randint(1, 10))) for _ in range(64)]
    knowledge = [[key, value] for key, value in zip(keys, rng.choices(values, k=K), strict=True)]
    parts = []
    for _ in range(PAIRS):
        if rng.random() < UNKNOWN:
            key = "".join(rng.choices(ascii_lowercase, k=5))
        else:
            key = keys[K - 1 - rng.randrange(TAIL)]
        parts.append(f"({key})")
        if rng.random() < 0.3:
            parts.append("".join(rng.choices(ascii_lowercase, k=rng.randint(1, 3))))
    return {"s": "".join(parts), "knowledge": knowledge}
