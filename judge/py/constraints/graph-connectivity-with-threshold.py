"""Graph Connectivity With Threshold: n cities, a threshold and pair queries."""


def check(n: int, threshold: int, queries: list[list[int]]) -> None:
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert 0 <= threshold <= n, "0 <= threshold <= n"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in queries), "1 <= ai, bi <= cities"
    assert all(a != b for a, b in queries), "ai != bi"
