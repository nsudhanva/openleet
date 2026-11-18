"""The Number of Beautiful Subsets: an array of positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 18, "1 <= nums.length <= 18"
    assert all(1 <= x <= 1000 for x in nums), "1 <= nums[i] <= 1000"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
