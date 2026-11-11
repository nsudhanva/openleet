"""Uncrossed Lines at 200 x 200 values over 20 symbols, so trying both skips at every mismatch
without memoizing is exponential while the DP is 4 * 10^4 cells."""

SEEDS = 2
N = 200


def generate(rng):
    return {
        "nums1": [rng.randint(1, 20) for _ in range(N)],
        "nums2": [rng.randint(1, 20) for _ in range(N)],
    }
