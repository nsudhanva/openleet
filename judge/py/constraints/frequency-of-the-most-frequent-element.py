"""Frequency of the Most Frequent Element: positive integers and an increment budget k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
