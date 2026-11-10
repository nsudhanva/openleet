"""Reverse String on 10^5 printable ASCII characters."""

SEEDS = 2
CHARS = [chr(c) for c in range(32, 127)]


def generate(rng):
    return {"s": [rng.choice(CHARS) for _ in range(10**5)]}
