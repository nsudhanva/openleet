"""Minimum Swaps to Group All 1's Together II at n = 10^5 with half the entries 1, so re-counting
each of the n circular windows of length 5 * 10^4 is ~5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [1] * (N // 2) + [0] * (N - N // 2)
    rng.shuffle(nums)
    return {"nums": nums}
