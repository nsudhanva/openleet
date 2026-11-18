"""Final Element After Subarray Deletions: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**5 for x in nums), "1 <= nums[i] <= 10^5"
