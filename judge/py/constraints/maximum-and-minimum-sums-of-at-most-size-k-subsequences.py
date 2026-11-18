"""Maximum and Minimum Sums of at Most Size K Subsequences: an array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 1 <= k <= min(70, len(nums)), "1 <= k <= min(70, nums.length)"
