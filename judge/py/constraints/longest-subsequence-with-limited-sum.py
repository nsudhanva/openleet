"""Longest Subsequence With Limited Sum: a list of integers and a list of queries."""


def check(nums: list[int], queries: list[int]) -> None:
    n, m = len(nums), len(queries)
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert all(1 <= v <= 10**6 for v in queries), "1 <= queries[i] <= 10^6"
