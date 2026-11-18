"""Find the Count of Monotonic Pairs I: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 2000, "1 <= n == nums.length <= 2000"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
