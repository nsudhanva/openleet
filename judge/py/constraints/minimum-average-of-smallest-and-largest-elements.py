"""Minimum Average of Smallest and Largest Elements: an even-length list of small integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 50, "2 <= n == nums.length <= 50"
    assert len(nums) % 2 == 0, "n is even"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
