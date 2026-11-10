"""Minimum Cost For Tickets with up to all 365 travel days and random pass prices."""

SEEDS = 3


def generate(rng):
    count = rng.choice((365, rng.randint(100, 364)))
    days = sorted(rng.sample(range(1, 366), count))
    return {"days": days, "costs": [rng.randint(1, 1000) for _ in range(3)]}
