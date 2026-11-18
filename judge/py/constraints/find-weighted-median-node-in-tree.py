"""Find Weighted Median Node in Tree: n nodes, weighted edges forming a tree, and node-pair
queries."""


def check(n: int, edges: list[list[int]], queries: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 3 for e in edges), "edges[i] == [ui, vi, wi]"
    assert all(0 <= e[0] < n and 0 <= e[1] < n for e in edges), "0 <= ui, vi < n"
    assert all(1 <= e[2] <= 10**9 for e in edges), "1 <= wi <= 10^9"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[j] == [uj, vj]"
    assert all(0 <= q[0] < n and 0 <= q[1] < n for q in queries), "0 <= uj, vj < n"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _ in edges:
        ru, rv = find(u), find(v)
        assert ru != rv, "edges represents a valid tree"
        parent[ru] = rv
