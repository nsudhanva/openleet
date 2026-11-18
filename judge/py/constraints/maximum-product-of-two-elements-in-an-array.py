"""Maximum Product of Two Elements in an Array: positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 500, "2 <= nums.length <= 500"
    assert all(1 <= v <= 10**3 for v in nums), "1 <= nums[i] <= 10^3"
