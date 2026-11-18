"""Average Value of Even Numbers That Are Divisible by Three: positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
