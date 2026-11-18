"""Find Closest Number to Zero: a list of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= n <= 1000"
    assert all(-(10**5) <= x <= 10**5 for x in nums), "-10^5 <= nums[i] <= 10^5"
