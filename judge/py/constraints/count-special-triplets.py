"""Count Special Triplets: a non-negative integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= n == nums.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
