"""Maximum Subarray Sum After Multiplier: an integer array and a positive factor k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
