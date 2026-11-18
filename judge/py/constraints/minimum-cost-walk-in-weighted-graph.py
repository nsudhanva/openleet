"""Minimum Cost Walk in Weighted Graph: n vertices, weighted edges and (start, end) queries."""


def check(n: int, edges: list[list[int]], query: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 0 <= len(edges) <= 10**5, "0 <= edges.length <= 10^5"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= e[0] <= n - 1 and 0 <= e[1] <= n - 1 for e in edges), "0 <= ui, vi <= n - 1"
    assert all(e[0] != e[1] for e in edges), "ui != vi"
    assert all(0 <= e[2] <= 10**5 for e in edges), "0 <= wi <= 10^5"
    assert 1 <= len(query) <= 10**5, "1 <= query.length <= 10^5"
    assert all(len(q) == 2 for q in query), "query[i].length == 2"
    assert all(0 <= q[0] <= n - 1 and 0 <= q[1] <= n - 1 for q in query), "0 <= si, ti <= n - 1"
    assert all(q[0] != q[1] for q in query), "si != ti"
