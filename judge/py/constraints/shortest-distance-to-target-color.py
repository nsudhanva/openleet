"""Shortest Distance to Target Color: colors 1..3 and [index, color] queries."""


def check(colors: list[int], queries: list[list[int]]) -> None:
    n = len(colors)
    assert 1 <= n <= 5 * 10**4, "1 <= colors.length <= 5*10^4"
    assert all(1 <= c <= 3 for c in colors), "1 <= colors[i] <= 3"
    assert 1 <= len(queries) <= 5 * 10**4, "1 <= queries.length <= 5*10^4"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= i < n for i, _ in queries), "0 <= queries[i][0] < colors.length"
    assert all(1 <= c <= 3 for _, c in queries), "1 <= queries[i][1] <= 3"
