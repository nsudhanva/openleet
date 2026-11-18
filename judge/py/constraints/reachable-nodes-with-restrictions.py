"""Reachable Nodes With Restrictions: a tree on n nodes and restricted nodes."""


def check(n: int, edges: list[list[int]], restricted: list[int]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "edges represents a valid tree"
        parent[ra] = rb
    assert 1 <= len(restricted) < n, "1 <= restricted.length < n"
    assert all(1 <= r < n for r in restricted), "1 <= restricted[i] < n"
    assert len(set(restricted)) == len(restricted), "all the values of restricted are unique"
