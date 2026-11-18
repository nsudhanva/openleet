"""Maximize the Number of Target Nodes After Connecting Trees II: two trees' edge lists."""


def _tree(edges: list[list[int]], name: str) -> None:
    n = len(edges) + 1
    assert 2 <= n <= 10**5, f"2 <= node count of {name} <= 10^5"
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


def check(edges1: list[list[int]], edges2: list[list[int]]) -> None:
    _tree(edges1, "edges1")
    _tree(edges2, "edges2")
