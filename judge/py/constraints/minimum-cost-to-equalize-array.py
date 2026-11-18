"""Minimum Cost to Equalize Array: an integer array and two operation costs."""


def check(nums: list[int], cost1: int, cost2: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**6 for x in nums), "1 <= nums[i] <= 10^6"
    assert 1 <= cost1 <= 10**6, "1 <= cost1 <= 10^6"
    assert 1 <= cost2 <= 10**6, "1 <= cost2 <= 10^6"
