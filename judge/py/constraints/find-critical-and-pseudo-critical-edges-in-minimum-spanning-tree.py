"""Find Critical and Pseudo-Critical Edges in MST: a connected weighted graph, edges [a, b, w]."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert 1 <= len(edges) <= min(200, n * (n - 1) // 2), (
        "1 <= edges.length <= min(200, n * (n - 1) / 2)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= a < b < n for a, b, _ in edges), "0 <= ai < bi < n"
    assert all(1 <= w <= 1000 for _, _, w in edges), "1 <= weighti <= 1000"
    assert len({(a, b) for a, b, _ in edges}) == len(edges), "all pairs (ai, bi) are distinct"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b, _ in edges:
        parent[find(a)] = find(b)
    assert len({find(x) for x in range(n)}) == 1, "the graph is connected"
