"""Minimum Cost For Tickets with up to all 365 travel days and random pass prices."""

SEEDS = 3
DAYS = 365
LOW = 100


def generate(rng):
    count = rng.choice((DAYS, rng.randint(LOW, DAYS - 1)))
    days = sorted(rng.sample(range(1, DAYS + 1), count))
    return {"days": days, "costs": [rng.randint(1, 1000) for _ in range(3)]}
