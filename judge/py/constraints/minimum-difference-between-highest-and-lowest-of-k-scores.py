"""Minimum Difference Between Highest and Lowest of K Scores: scores and a group size k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 1000, "1 <= k <= nums.length <= 1000"
    assert all(0 <= x <= 10**5 for x in nums), "0 <= nums[i] <= 10^5"
