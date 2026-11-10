"""Smallest Stable Index I on 100 values in [0, 10^9]: answer late, or none."""

SEEDS = 2


def generate(rng):
    nums = sorted((rng.randint(0, 10**9) for _ in range(100)), reverse=True)
    k = rng.choice([0, rng.randint(0, 10**9)])
    return {"nums": nums, "k": k}
