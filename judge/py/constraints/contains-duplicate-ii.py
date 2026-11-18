"""Contains Duplicate II: a list of integers and a distance k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert isinstance(k, int), "k is an integer"
    assert 0 <= k <= 10**5, "0 <= k <= 10^5"
