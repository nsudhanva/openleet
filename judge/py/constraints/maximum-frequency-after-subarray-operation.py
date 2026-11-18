"""Maximum Frequency After Subarray Operation: an array of values 1..50 and a target k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
    assert 1 <= k <= 50, "1 <= k <= 50"
