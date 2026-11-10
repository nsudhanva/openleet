"""Sum of Variable Length Subarrays at the maximum n = 100 with values up to 1000."""

SEEDS = 2
N = 100


def generate(rng):
    return {"nums": [rng.randint(1, 1000) for _ in range(N)]}
