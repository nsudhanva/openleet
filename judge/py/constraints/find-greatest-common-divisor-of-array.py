"""Find Greatest Common Divisor of Array: a list of small positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 1000, "2 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
