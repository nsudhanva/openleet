"""Largest Number with 100 values that share prefixes (3, 30, 34, 303, ...) so plain string
sorting is wrong; one seed is all zeros."""

SEEDS = 3
N = 100


def generate(rng):
    shape = rng.choice(["prefix", "random", "zeros"])
    if shape == "zeros":
        return {"nums": [0] * N}
    if shape == "random":
        return {"nums": [rng.randint(0, 10**9) for _ in range(N)]}
    nums = []
    for _ in range(N):
        stem = rng.choice(["3", "30", "34", "9", "98", "121", "12"])
        v = int((stem * rng.randint(1, 4))[: rng.randint(1, 9)])
        nums.append(v)
    return {"nums": nums}
