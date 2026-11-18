"""Checking Existence of Edge Length Limited Paths: n, weighted edges, queries."""


def check(n: int, edgeList: list[list[int]], queries: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(edgeList) <= 10**5, "1 <= edgeList.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(e) == 3 for e in edgeList), "edgeList[i].length == 3"
    assert all(len(q) == 3 for q in queries), "queries[j].length == 3"
    assert all(0 <= e[0] <= n - 1 and 0 <= e[1] <= n - 1 for e in edgeList), "0 <= ui, vi <= n - 1"
    assert all(0 <= q[0] <= n - 1 and 0 <= q[1] <= n - 1 for q in queries), "0 <= pj, qj <= n - 1"
    assert all(e[0] != e[1] for e in edgeList), "ui != vi"
    assert all(q[0] != q[1] for q in queries), "pj != qj"
    assert all(1 <= e[2] <= 10**9 for e in edgeList), "1 <= disi <= 10^9"
    assert all(1 <= q[2] <= 10**9 for q in queries), "1 <= limitj <= 10^9"
