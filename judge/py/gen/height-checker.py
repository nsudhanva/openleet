"""Height Checker at n = 100 with heights in [1, 100]."""

SEEDS = 2


def generate(rng):
    hi = rng.choice([3, 100])
    return {"heights": [rng.randint(1, hi) for _ in range(100)]}
