"""Greatest Sum Divisible by Three: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 4 * 10**4, "1 <= nums.length <= 4 * 10^4"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
