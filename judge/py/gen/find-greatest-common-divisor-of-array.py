"""Find GCD of Array at n = 1000 with values up to 1000."""

SEEDS = 2


def generate(rng):
    step = rng.choice([1, 7, 12])
    return {"nums": [rng.randint(1, 1000 // step) * step for _ in range(1000)]}
