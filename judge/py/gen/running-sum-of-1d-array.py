"""Running Sum on 1000 values in [-10^6, 10^6]."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(-(10**6), 10**6) for _ in range(1000)]}
