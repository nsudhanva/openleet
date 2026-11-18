"""Minimize the Maximum Difference of Pairs: a list of integers and a pair count p."""


def check(nums: list[int], p: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= p <= len(nums) // 2, "0 <= p <= nums.length / 2"
