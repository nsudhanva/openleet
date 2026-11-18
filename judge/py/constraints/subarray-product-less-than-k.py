"""Subarray Product Less Than K: positive integers and a bound k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(isinstance(v, int) and 1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert isinstance(k, int) and 0 <= k <= 10**6, "0 <= k <= 10^6"
