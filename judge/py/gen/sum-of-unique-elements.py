"""Sum of Unique Elements at the maximum n = 100 with a mix of singletons and repeats."""

SEEDS = 2
N = 100


def generate(rng):
    pool = rng.randint(30, 100)
    return {"nums": [rng.randint(1, pool) for _ in range(N)]}
