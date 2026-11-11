"""Length of the Longest Subsequence That Sums to Target with 500 small values and target near
1000, so the O(n * target) DP is 5 * 10^5 steps while tracking every (sum, length) pair is
~2.5 * 10^8."""

SEEDS = 2
N = 500
TARGET = 1000


def generate(rng):
    top = rng.randint(20, 40)
    nums = [rng.randint(1, top) for _ in range(N)]
    return {"nums": nums, "target": TARGET - rng.randint(0, 9)}
