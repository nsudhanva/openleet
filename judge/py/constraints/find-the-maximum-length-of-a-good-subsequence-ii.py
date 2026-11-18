"""Find the Maximum Length of a Good Subsequence II: an array and a limit k on changes."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 5 * 10**3, "1 <= nums.length <= 5 * 10^3"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= k <= min(50, len(nums)), "0 <= k <= min(50, nums.length)"
