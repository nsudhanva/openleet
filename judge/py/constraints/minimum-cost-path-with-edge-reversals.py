"""Minimum Cost Path with Edge Reversals: n nodes and weighted directed edges [u, v, w]."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert 1 <= len(edges) <= 10**5, "1 <= edges.length <= 10^5"
    assert all(len(e) == 3 for e in edges), "edges[i] = [ui, vi, wi]"
    assert all(0 <= e[0] <= n - 1 and 0 <= e[1] <= n - 1 for e in edges), "0 <= ui, vi <= n - 1"
    assert all(1 <= e[2] <= 1000 for e in edges), "1 <= wi <= 1000"
