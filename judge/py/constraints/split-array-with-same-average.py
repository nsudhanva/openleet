"""Split Array With Same Average: a short array of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 30, "1 <= nums.length <= 30"
    assert all(0 <= v <= 10**4 for v in nums), "0 <= nums[i] <= 10^4"
