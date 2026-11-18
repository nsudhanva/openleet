"""Find Root of a Colored Tree: an undirected tree of max degree 3 with node colors."""


def check(edges: list[list[int]], colors: str) -> None:
    n = len(colors)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i] = [ui, vi]"
    assert all(0 <= u < n and 0 <= v < n for u, v in edges), "0 <= ui, vi < n"
    assert all(c in "RBW" for c in colors), "colors[i] is one of 'R', 'B', 'W'"
    deg = [0] * n
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
        ru, rv = find(u), find(v)
        assert ru != rv, "the input graph is a tree"
        parent[ru] = rv
    assert max(deg) <= 3, "every node has degree at most three"
