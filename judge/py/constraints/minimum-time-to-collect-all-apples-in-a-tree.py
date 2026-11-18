"""Minimum Time to Collect All Apples in a Tree: an undirected tree and apple flags."""


def check(n: int, edges: list[list[int]], hasApple: list[bool]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < b <= n - 1 for a, b in edges), "0 <= ai < bi <= n - 1"
    assert len(hasApple) == n, "hasApple.length == n"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the edges form a tree"
        parent[ra] = rb
