"""Minimum Height Trees: n nodes and the undirected edges of a tree."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), (
        "all the pairs (ai, bi) are distinct"
    )
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the input is a tree"
        parent[ra] = rb
