"""Third Maximum Number: a list of 32-bit integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(2**31) <= x <= 2**31 - 1 for x in nums), "-2^31 <= nums[i] <= 2^31 - 1"
