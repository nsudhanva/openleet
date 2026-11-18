"""Minimum Degree of a Connected Trio in a Graph: n nodes numbered 1..n and undirected edges."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 400, "2 <= n <= 400"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert 1 <= len(edges) <= n * (n - 1) // 2, "1 <= edges.length <= n * (n-1) / 2"
    assert all(1 <= e[0] <= n and 1 <= e[1] <= n for e in edges), "1 <= ui, vi <= n"
    assert all(e[0] != e[1] for e in edges), "ui != vi"
    assert len({frozenset(e) for e in edges}) == len(edges), "there are no repeated edges"
