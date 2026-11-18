"""Minimum Edge Reversals So Every Node Is Reachable: n nodes and directed tree edges."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= u < n and 0 <= v < n for u, v in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v in edges), "ui != vi"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the graph is a tree if edges were bi-directional"
        parent[ra] = rb
