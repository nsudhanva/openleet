"""Remove Max Number of Edges to Keep Graph Fully Traversable: typed undirected edges on n nodes."""


def check(n: int, edges: list[list[int]]) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(edges) <= min(10**5, 3 * n * (n - 1) // 2), (
        "1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(1 <= t <= 3 for t, _, _ in edges), "1 <= typei <= 3"
    assert all(1 <= u < v <= n for _, u, v in edges), "1 <= ui < vi <= n"
    assert len({tuple(e) for e in edges}) == len(edges), "all tuples (typei, ui, vi) are distinct"
