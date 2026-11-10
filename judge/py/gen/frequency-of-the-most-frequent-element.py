"""Frequency of the Most Frequent Element at n = 10^5, values up to 10^5, k across its range."""

SEEDS = 3
N = 10**5


def generate(rng):
    hi = rng.choice([100, 10**5])
    nums = [rng.randint(1, hi) for _ in range(N)]
    return {"nums": nums, "k": rng.choice([1, 10**5, rng.randint(1, 10**5)])}
