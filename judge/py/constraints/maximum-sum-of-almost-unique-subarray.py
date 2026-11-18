"""Maximum Sum of Almost Unique Subarray: a positive integer array and window parameters m, k."""


def check(nums: list[int], m: int, k: int) -> None:
    assert 1 <= len(nums) <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert 1 <= m <= k <= len(nums), "1 <= m <= k <= nums.length"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
