"""Minimize Maximum Component Cost: a connected weighted undirected graph and a limit k."""


def check(n: int, edges: list[list[int]], k: int) -> None:
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert 0 <= len(edges) <= 10**5, "0 <= edges.length <= 10^5"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= u < n and 0 <= v < n for u, v, _ in edges), "0 <= ui, vi < n"
    assert all(1 <= w <= 10**6 for _, _, w in edges), "1 <= wi <= 10^6"
    assert 1 <= k <= n, "1 <= k <= n"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    for u, v, _ in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            comps -= 1
    assert comps == 1, "the input graph is connected"
