"""Minimum Increment Operations to Make Array Beautiful at n = 60 with every value below k:
choosing which elements to raise, one of the next three each time, without memoization is
~10^15 choices."""

SEEDS = 2
N = 60


def generate(rng):
    k = rng.randint(10**8, 10**9)
    return {"nums": [rng.randint(0, k - 1) for _ in range(N)], "k": k}
