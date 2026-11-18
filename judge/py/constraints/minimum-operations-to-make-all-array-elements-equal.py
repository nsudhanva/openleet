"""Minimum Operations to Make All Array Elements Equal: positive integers and queries."""


def check(nums: list[int], queries: list[int]) -> None:
    assert isinstance(nums, list) and isinstance(queries, list), "nums and queries are lists"
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= m <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
    assert all(1 <= q <= 10**9 for q in queries), "1 <= queries[i] <= 10^9"
