"""Minimum Adjacent Swaps for K Consecutive Ones at n = 10^5 with about 90% ones and k half of
them, so pricing each window of k ones from scratch is about 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = [int(rng.random() < 0.9) for _ in range(N)]
    nums[0] = 1
    return {"nums": nums, "k": max(1, sum(nums) // 2)}
