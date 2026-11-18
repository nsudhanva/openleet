"""Sum of Absolute Differences in a Sorted Array: a non-decreasing integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**4 for x in nums), "1 <= nums[i] <= 10^4"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), "nums[i] <= nums[i + 1]"
