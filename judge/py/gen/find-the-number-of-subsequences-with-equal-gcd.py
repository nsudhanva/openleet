"""Subsequence pairs with equal GCD at the maximum n = 200 with values up to 200, either random or
built from multiples of a few small numbers so many GCDs coincide."""

SEEDS = 3


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 200) for _ in range(200)]
    else:
        base = rng.choice([2, 3, 6])
        nums = [base * rng.randint(1, 200 // base) for _ in range(200)]
    return {"nums": nums}
