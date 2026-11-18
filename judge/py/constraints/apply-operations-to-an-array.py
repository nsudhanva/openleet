"""Apply Operations to an Array: small non-negative integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2000, "2 <= nums.length <= 2000"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
