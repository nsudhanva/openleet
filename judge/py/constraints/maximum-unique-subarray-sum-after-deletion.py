"""Maximum Unique Subarray Sum After Deletion: a small array of ints."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
