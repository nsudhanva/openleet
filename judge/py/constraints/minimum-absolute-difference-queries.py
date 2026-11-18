"""Minimum Absolute Difference Queries: a list of small integers and [l, r] subarray queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= len(queries) <= 2 * 10**4, "1 <= queries.length <= 2 * 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= lo < r < n for lo, r in queries), "0 <= li < ri < nums.length"
