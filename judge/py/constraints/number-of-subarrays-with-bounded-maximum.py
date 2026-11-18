"""Number of Subarrays with Bounded Maximum: an integer array and bounds left <= right."""


def check(nums: list[int], left: int, right: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= left <= right <= 10**9, "0 <= left <= right <= 10^9"
