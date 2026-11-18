"""Number of Good Paths: node values and the edges of a tree."""


def check(vals: list[int], edges: list[list[int]]) -> None:
    n = len(vals)
    assert 1 <= n <= 3 * 10**4, "1 <= n <= 3 * 10^4"
    assert all(0 <= v <= 10**5 for v in vals), "0 <= vals[i] <= 10^5"
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
