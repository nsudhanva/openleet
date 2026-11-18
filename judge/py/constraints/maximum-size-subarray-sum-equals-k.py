"""Maximum Size Subarray Sum Equals k: an integer array and a target sum."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 2 * 10**5, "1 <= nums.length <= 2 * 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert -(10**9) <= k <= 10**9, "-10^9 <= k <= 10^9"
