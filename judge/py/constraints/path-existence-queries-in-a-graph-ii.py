"""Path Existence Queries in a Graph II: n nodes with values, maxDiff and node-pair queries."""


def check(n: int, nums: list[int], maxDiff: int, queries: list[list[int]]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert isinstance(n, int) and 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert n == len(nums), "n == nums.length"
    assert all(isinstance(v, int) and 0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert isinstance(maxDiff, int) and 0 <= maxDiff <= 10**5, "0 <= maxDiff <= 10^5"
    assert isinstance(queries, list), "queries is an array"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i] == [ui, vi]"
    assert all(isinstance(x, int) and 0 <= x < n for q in queries for x in q), "0 <= ui, vi < n"
