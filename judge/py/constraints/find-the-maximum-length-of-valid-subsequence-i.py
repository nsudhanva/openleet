"""Find the Maximum Length of Valid Subsequence I: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2 * 10**5, "2 <= nums.length <= 2 * 10^5"
    assert all(1 <= v <= 10**7 for v in nums), "1 <= nums[i] <= 10^7"
