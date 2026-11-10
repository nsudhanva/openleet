"""Freedom Trail at the maximum lengths (ring and key of 100) over a tiny alphabet, so every key
letter has many ring positions to choose from."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 3


def generate(rng):
    alpha = ascii_lowercase[: rng.choice([2, 3, 26])]
    ring = [rng.choice(alpha) for _ in range(100)]
    ring[: len(alpha)] = alpha
    rng.shuffle(ring)
    key = random_string(rng, alpha, 100)
    return {"ring": "".join(ring), "key": key}
