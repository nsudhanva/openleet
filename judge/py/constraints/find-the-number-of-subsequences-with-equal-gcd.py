"""Find the Number of Subsequences With Equal GCD: a short array of integers up to 200."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(1 <= v <= 200 for v in nums), "1 <= nums[i] <= 200"
