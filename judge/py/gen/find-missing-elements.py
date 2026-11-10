"""Find Missing Elements with up to 100 unique values in [1, 100]."""

SEEDS = 2


def generate(rng):
    n = rng.randint(2, 100)
    nums = rng.sample(range(1, 101), n)
    return {"nums": nums}
