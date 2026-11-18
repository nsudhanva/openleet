"""Length of the Longest Subsequence That Sums to Target: an integer array and a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert 1 <= target <= 1000, "1 <= target <= 1000"
