"""Maximize Spanning Tree Stability with Upgrades: n nodes, edges [u, v, s, must], k."""


def check(n: int, edges: list[list[int]], k: int) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(edges) <= 10**5, "1 <= edges.length <= 10^5"
    assert all(len(e) == 4 for e in edges), "edges[i] = [ui, vi, si, musti]"
    assert all(0 <= u < n and 0 <= v < n for u, v, _, _ in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v, _, _ in edges), "ui != vi"
    assert all(1 <= s <= 10**5 for _, _, s, _ in edges), "1 <= si <= 10^5"
    assert all(m in (0, 1) for _, _, _, m in edges), "musti is either 0 or 1"
    assert 0 <= k <= n, "0 <= k <= n"
    assert len({(min(u, v), max(u, v)) for u, v, _, _ in edges}) == len(edges), (
        "There are no duplicate edges"
    )
