"""Number of Subsequences That Satisfy the Given Sum Condition: an integer array and a target."""


def check(nums: list[int], target: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert 1 <= target <= 10**6, "1 <= target <= 10^6"
