"""Find All K-Distant Indices in an Array: nums, a key from nums, and k."""


def check(nums: list[int], key: int, k: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= x <= 1000 for x in nums), "1 <= nums[i] <= 1000"
    assert key in nums, "key is an integer from the array nums"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
