"""Reverse Only Letters on 100-character strings mixing letters and symbols (no quote or
backslash)."""

SEEDS = 2
CHARS = [chr(c) for c in range(33, 123) if chr(c) not in '"\\']


def generate(rng):
    return {"s": "".join(rng.choice(CHARS) for _ in range(100))}
