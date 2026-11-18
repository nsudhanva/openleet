"""Graph Valid Tree: n nodes and a list of undirected edges."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 2000, "1 <= n <= 2000"
    assert 0 <= len(edges) <= 5000, "0 <= edges.length <= 5000"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), "no repeated edges"
