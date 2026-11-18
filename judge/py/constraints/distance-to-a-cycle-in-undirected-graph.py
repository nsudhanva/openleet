"""Distance to a Cycle in Undirected Graph: a connected graph with n nodes and n edges."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert len(edges) == n, "edges.length == n"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in edges), (
        "0 <= node1i, node2i <= n - 1"
    )
    assert all(a != b for a, b in edges), "node1i != node2i"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == n, "at most one edge between any pair"
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    assert len({find(i) for i in range(n)}) == 1, "the graph is connected"
    # connected with n nodes and n edges means exactly one cycle
