"""Find Building Where Alice and Bob Can Meet: building heights and (Alice, Bob) queries."""


def check(heights: list[int], queries: list[list[int]]) -> None:
    n = len(heights)
    assert 1 <= n <= 5 * 10**4, "1 <= heights.length <= 5 * 10^4"
    assert all(1 <= h <= 10**9 for h in heights), "1 <= heights[i] <= 10^9"
    assert 1 <= len(queries) <= 5 * 10**4, "1 <= queries.length <= 5 * 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i] = [ai, bi]"
    assert all(0 <= x <= n - 1 for q in queries for x in q), "0 <= ai, bi <= heights.length - 1"
