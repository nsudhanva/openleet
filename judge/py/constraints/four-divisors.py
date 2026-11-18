"""Four Divisors: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
