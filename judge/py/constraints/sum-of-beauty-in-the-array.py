"""Sum of Beauty in the Array: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**5 for x in nums), "1 <= nums[i] <= 10^5"
