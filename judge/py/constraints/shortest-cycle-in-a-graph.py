"""Shortest Cycle in a Graph: n vertices and an undirected edge list without repeats."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 1 <= len(edges) <= 1000, "1 <= edges.length <= 1000"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= u < n and 0 <= v < n for u, v in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v in edges), "ui != vi"
    assert len({(min(u, v), max(u, v)) for u, v in edges}) == len(edges), (
        "There are no repeated edges"
    )
