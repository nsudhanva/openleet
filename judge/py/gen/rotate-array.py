"""Rotate Array at n = 10^5 with full 32-bit values and k anywhere in [0, 10^5] (often k >= n
or k = n - 1, punishing one-step-at-a-time rotation)."""

SEEDS = 3


def generate(rng):
    n = rng.choice([10**5, rng.randint(1000, 10**5 - 1)])
    nums = [rng.randint(-(2**31), 2**31 - 1) for _ in range(n)]
    k = rng.choice([n - 1, rng.randint(0, 10**5), 10**5])
    return {"nums": nums, "k": k}
