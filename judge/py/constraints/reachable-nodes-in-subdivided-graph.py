"""Reachable Nodes In Subdivided Graph: weighted edges [u, v, cnt], maxMoves and n nodes."""


def check(edges: list[list[int]], maxMoves: int, n: int) -> None:
    assert 1 <= n <= 3000, "1 <= n <= 3000"
    assert 0 <= len(edges) <= min(n * (n - 1) // 2, 10**4), (
        "0 <= edges.length <= min(n * (n - 1) / 2, 10^4)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= u < v < n for u, v, _ in edges), "0 <= ui < vi < n"
    assert len({(u, v) for u, v, _ in edges}) == len(edges), "no multiple edges"
    assert all(0 <= c <= 10**4 for _, _, c in edges), "0 <= cnti <= 10^4"
    assert 0 <= maxMoves <= 10**9, "0 <= maxMoves <= 10^9"
