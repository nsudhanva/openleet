"""Maximum Difference Between Increasing Elements: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 1000, "2 <= n <= 1000"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
