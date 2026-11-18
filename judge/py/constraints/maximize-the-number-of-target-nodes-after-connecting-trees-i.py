"""Maximize the Number of Target Nodes After Connecting Trees I: two trees' edge lists and k."""


def _tree(edges: list[list[int]], name: str) -> None:
    n = len(edges) + 1
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), f"0 <= {name} endpoints < node count"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, f"{name} represents a valid tree"
        parent[ra] = rb


def check(edges1: list[list[int]], edges2: list[list[int]], k: int) -> None:
    assert 2 <= len(edges1) + 1 <= 1000, "2 <= n <= 1000 (edges1.length == n - 1)"
    assert 2 <= len(edges2) + 1 <= 1000, "2 <= m <= 1000 (edges2.length == m - 1)"
    _tree(edges1, "edges1")
    _tree(edges2, "edges2")
    assert 0 <= k <= 1000, "0 <= k <= 1000"
