"""Maximum Good Subarray Sum: an integer array and a difference k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
