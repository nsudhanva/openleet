"""Maximum Score After Applying Operations on a Tree: tree edges and node values."""


def check(edges: list[list[int]], values: list[int]) -> None:
    n = len(values)
    assert 2 <= n <= 2 * 10**4, "2 <= n <= 2 * 10^4"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(1 <= v <= 10**9 for v in values), "1 <= values[i] <= 10^9"
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
