"""Smaller Numbers Than Current at n = 500 with values in [0, 100] (many ties)."""

SEEDS = 2


def generate(rng):
    hi = rng.choice([5, 100])
    return {"nums": [rng.randint(0, hi) for _ in range(500)]}
