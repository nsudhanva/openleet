"""Maximum Subtree of the Same Color: tree edges on nodes 0..n-1 and a color per node."""


def check(edges: list[list[int]], colors: list[int]) -> None:
    n = len(edges) + 1
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(len(e) == 2 for e in edges), "edges[i] == [ui, vi]"
    assert all(0 <= u < n and 0 <= v < n for u, v in edges), "0 <= ui, vi < n"
    assert len(colors) == n, "colors.length == n"
    assert all(1 <= c <= 10**5 for c in colors), "1 <= colors[i] <= 10^5"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        assert ru != rv, "the graph represented by edges is a tree"
        parent[ru] = rv
