"""Redundant Connection: n edges over nodes 1..n forming a tree plus one extra edge."""


def check(edges: list[list[int]]) -> None:
    n = len(edges)
    assert 3 <= n <= 1000, "3 <= n <= 1000"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= a < b <= n for a, b in edges), "1 <= ai < bi <= edges.length"
    assert len({tuple(e) for e in edges}) == n, "there are no repeated edges"
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    assert len({find(v) for v in range(1, n + 1)}) == 1, "the given graph is connected"
