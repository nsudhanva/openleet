"""Tree Diameter: the edges of an undirected tree on nodes 0..n-1."""


def check(edges: list[list[int]]) -> None:
    n = len(edges) + 1
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
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
        assert ra != rb, "the edges form a tree (no cycle, no duplicate edge)"
        parent[ra] = rb
