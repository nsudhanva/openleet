"""Length of Longest Subarray With at Most K Frequency: an integer array and a limit k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
