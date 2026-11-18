"""Jump Game: an array of maximum jump lengths."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
