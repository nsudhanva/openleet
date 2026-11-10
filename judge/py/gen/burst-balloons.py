"""Burst Balloons at the maximum n = 300 (cubic interval DP), with random values that include
zeros, or all values high."""

SEEDS = 2
N = 300


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(0, 100) for _ in range(N)]
    else:
        nums = [rng.randint(90, 100) for _ in range(N)]
    return {"nums": nums}
