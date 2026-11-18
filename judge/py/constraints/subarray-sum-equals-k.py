"""Subarray Sum Equals K: integers and a target k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(isinstance(v, int) and -1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
    assert isinstance(k, int) and -(10**7) <= k <= 10**7, "-10^7 <= k <= 10^7"
