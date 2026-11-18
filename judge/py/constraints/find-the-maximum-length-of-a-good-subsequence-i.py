"""Find the Maximum Length of a Good Subsequence I: an array and a limit k on changes."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 500, "1 <= nums.length <= 500"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= k <= min(len(nums), 25), "0 <= k <= min(nums.length, 25)"
