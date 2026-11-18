"""Find if Path Exists in Graph: n vertices, an undirected edge list, a source and a
destination."""


def check(n: int, edges: list[list[int]], source: int, destination: int) -> None:
    assert 1 <= n <= 2 * 10**5, "1 <= n <= 2 * 10^5"
    assert 0 <= len(edges) <= 2 * 10**5, "0 <= edges.length <= 2 * 10^5"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= u <= n - 1 and 0 <= v <= n - 1 for u, v in edges), "0 <= ui, vi <= n - 1"
    assert all(u != v for u, v in edges), "ui != vi (no self edges)"
    assert len({(min(u, v), max(u, v)) for u, v in edges}) == len(edges), "no duplicate edges"
    assert 0 <= source <= n - 1, "0 <= source <= n - 1"
    assert 0 <= destination <= n - 1, "0 <= destination <= n - 1"
