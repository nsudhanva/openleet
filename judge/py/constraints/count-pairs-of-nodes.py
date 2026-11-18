"""Count Pairs of Nodes: n nodes, an undirected edge list (1-indexed), and queries."""


def check(n: int, edges: list[list[int]], queries: list[int]) -> None:
    assert 2 <= n <= 2 * 10**4, "2 <= n <= 2 * 10^4"
    assert 1 <= len(edges) <= 10**5, "1 <= edges.length <= 10^5"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in edges), "1 <= ui, vi <= n"
    assert all(u != v for u, v in edges), "ui != vi"
    assert 1 <= len(queries) <= 20, "1 <= queries.length <= 20"
    assert all(0 <= q < len(edges) for q in queries), "0 <= queries[j] < edges.length"
