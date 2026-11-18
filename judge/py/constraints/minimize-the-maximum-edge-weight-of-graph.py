"""Minimize the Maximum Edge Weight of Graph: a directed weighted graph and a threshold."""


def check(n: int, edges: list[list[int]], threshold: int) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= threshold <= n - 1, "1 <= threshold <= n - 1"
    assert 1 <= len(edges) <= min(10**5, n * (n - 1) // 2), (
        "1 <= edges.length <= min(10^5, n * (n - 1) / 2)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= a < n and 0 <= b < n for a, b, _ in edges), "0 <= Ai, Bi < n"
    assert all(a != b for a, b, _ in edges), "Ai != Bi"
    assert all(1 <= w <= 10**6 for _, _, w in edges), "1 <= Wi <= 10^6"
    seen = {(a, b, w) for a, b, w in edges}
    assert len(seen) == len(edges), "multiple edges between a pair must have unique weights"
