"""Find the Last Marked Nodes in Tree: the edges of an undirected tree on n nodes."""


def check(edges: list[list[int]]) -> None:
    assert isinstance(edges, list), "edges is an array"
    n = len(edges) + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5, edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= v <= n - 1 for e in edges for v in e), "0 <= edges[i][0], edges[i][1] <= n - 1"
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
