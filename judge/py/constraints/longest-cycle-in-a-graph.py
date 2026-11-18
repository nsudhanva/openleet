"""Longest Cycle in a Graph: a functional graph where edges[i] is the next node or -1."""


def check(edges: list[int]) -> None:
    n = len(edges)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(-1 <= e < n for e in edges), "-1 <= edges[i] < n"
    assert all(e != i for i, e in enumerate(edges)), "edges[i] != i"
