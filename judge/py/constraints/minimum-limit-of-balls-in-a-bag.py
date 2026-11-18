"""Minimum Limit of Balls in a Bag: bag sizes and a maximum number of operations."""


def check(nums: list[int], maxOperations: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= maxOperations <= 10**9, "1 <= maxOperations <= 10^9"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
