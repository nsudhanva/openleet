"""Count the Number of Complete Components: an undirected graph given as an edge list."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert 0 <= len(edges) <= n * (n - 1) // 2, "0 <= edges.length <= n * (n - 1) / 2"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in edges), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), (
        "there are no repeated edges"
    )
