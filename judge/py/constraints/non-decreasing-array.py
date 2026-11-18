"""Non-decreasing Array: an array of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= n <= 10^4"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
