"""Minimum Increment Operations to Make Array Beautiful at n = 2 * 10^4 with every value below k:
choosing which elements to raise, one of the next three each time, without memoization is
exponential, and a DP that scans every earlier index is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    k = rng.randint(10**8, 10**9)
    return {"nums": [rng.randint(0, k - 1) for _ in range(N)], "k": k}
