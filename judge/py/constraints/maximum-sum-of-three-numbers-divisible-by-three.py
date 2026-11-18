"""Maximum Sum of Three Numbers Divisible by Three: an array of positive ints."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
