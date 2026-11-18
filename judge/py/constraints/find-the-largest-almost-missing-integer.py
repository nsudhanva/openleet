"""Find the Largest Almost Missing Integer: an integer array and a subarray length k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(0 <= v <= 50 for v in nums), "0 <= nums[i] <= 50"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
