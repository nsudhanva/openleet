"""Number of Ways to Assign Edge Weights I: the edges of a tree on nodes 1..n."""


def check(edges: list[list[int]]) -> None:
    assert isinstance(edges, list), "edges is a list"
    n = len(edges) + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5 and edges.length == n - 1"
    assert all(isinstance(e, list) and len(e) == 2 for e in edges), "edges[i] == [ui, vi]"
    assert all(type(x) is int for e in edges for x in e), "edges[i] holds integers"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in edges), "1 <= ui, vi <= n"
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        assert ru != rv, "edges represents a valid tree"
        parent[ru] = rv
