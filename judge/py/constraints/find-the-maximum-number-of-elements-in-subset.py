"""Find the Maximum Number of Elements in Subset: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
