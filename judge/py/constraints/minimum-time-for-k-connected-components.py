"""Minimum Time for K Connected Components: n nodes, timed undirected edges, and k."""


def check(n: int, edges: list[list[int]], k: int) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 0 <= len(edges) <= 10**5, "0 <= edges.length <= 10^5"
    assert all(len(e) == 3 for e in edges), "edges[i] = [ui, vi, timei]"
    assert all(0 <= u < n and 0 <= v < n for u, v, _ in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v, _ in edges), "ui != vi"
    assert all(1 <= t <= 10**9 for _, _, t in edges), "1 <= timei <= 10^9"
    assert 1 <= k <= n, "1 <= k <= n"
    seen = {(min(u, v), max(u, v)) for u, v, _ in edges}
    assert len(seen) == len(edges), "There are no duplicate edges"
