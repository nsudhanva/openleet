"""Frog Position After T Seconds: an undirected tree on vertices 1..n, a time t and a target."""


def check(n: int, edges: list[list[int]], t: int, target: int) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in edges), "1 <= ai, bi <= n"
    assert 1 <= t <= 50, "1 <= t <= 50"
    assert 1 <= target <= n, "1 <= target <= n"
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the edges form a tree (no cycle)"
        parent[ra] = rb
