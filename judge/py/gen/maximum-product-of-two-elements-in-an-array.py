"""Maximum Product of Two Elements at the maximum n = 500 with values in [1, 1000]."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(1, 1000) for _ in range(500)]}
