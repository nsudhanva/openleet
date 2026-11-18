"""Smallest Missing Non-negative Integer After Operations: integers and a step value."""


def check(nums: list[int], value: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= value <= 10**5, "1 <= value <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
