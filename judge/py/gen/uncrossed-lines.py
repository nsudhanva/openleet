"""Uncrossed Lines at 500 x 500 values over 4 to 10 symbols, so trying both skips at every
mismatch without memoizing is exponential, the DP is 2.5 * 10^5 cells, and a DP over every pair of
equal values is ~(2.5 * 10^5 / symbols)^2 / 2 ~ 10^9 steps."""

SEEDS = 2
N = 500


def generate(rng):
    symbols = rng.randint(4, 10)
    return {
        "nums1": [rng.randint(1, symbols) for _ in range(N)],
        "nums2": [rng.randint(1, symbols) for _ in range(N)],
    }
