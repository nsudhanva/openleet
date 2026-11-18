"""Minimum Moves to Equal Array Elements: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert sum(nums) - min(nums) * len(nums) < 2**31, (
        "The answer is guaranteed to fit in a 32-bit integer"
    )
