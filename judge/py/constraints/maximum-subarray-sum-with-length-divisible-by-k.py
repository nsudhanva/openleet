"""Maximum Subarray Sum With Length Divisible by K: an integer array and a divisor k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 2 * 10**5, "1 <= k <= nums.length <= 2 * 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
