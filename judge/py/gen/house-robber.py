"""House Robber at the maximum n = 100 with values in [0, 400]."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(0, 400) for _ in range(100)]}
