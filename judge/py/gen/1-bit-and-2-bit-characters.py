"""1-bit and 2-bit Characters at length 1000 ending in 0: long runs of 1s before the final 0
decide the answer by parity, so scanning from the wrong place goes astray."""

SEEDS = 3


def generate(rng):
    n = 1000
    if rng.random() < 0.5:
        ones = rng.randrange(n - 1, 0, -1) if rng.random() < 0.5 else n - 1
        bits = [rng.randint(0, 1) for _ in range(n - 1 - ones)] + [1] * ones + [0]
    else:
        bits = [rng.randint(0, 1) for _ in range(n - 1)] + [0]
    return {"bits": bits}
