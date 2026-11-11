"""Minimum Operations to Make a Subsequence with target and arr of length 10^4, arr drawn mostly
from target, so the longest increasing run of target positions found by the quadratic LIS DP
costs ~4 * 10^7 steps against patience sorting."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    target = rng.sample(range(1, LIMIT + 1), N)
    arr = [rng.choice(target) if rng.random() < 0.9 else rng.randint(1, LIMIT) for _ in range(N)]
    return {"target": target, "arr": arr}
