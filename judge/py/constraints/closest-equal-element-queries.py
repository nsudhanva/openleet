"""Closest Equal Element Queries: a circular array and index queries."""


def check(nums: list[int], queries: list[int]) -> None:
    assert 1 <= len(queries) <= len(nums) <= 10**5, "1 <= queries.length <= nums.length <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert all(0 <= q < len(nums) for q in queries), "0 <= queries[i] < nums.length"
