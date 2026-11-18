"""Number of Connected Components in an Undirected Graph: node count and distinct edges."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 2000, "1 <= n <= 2000"
    assert 1 <= len(edges) <= 5000, "1 <= edges.length <= 5000"
    assert all(len(e) == 2 for e in edges), "edges[i] = [ai, bi]"
    assert all(0 <= v <= n - 1 for e in edges for v in e), "nodes are labeled 0 to n - 1"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), (
        "there are no repeated edges"
    )
