"""Find Closest Node to Given Two Nodes: a functional graph (edges[i] or -1) and two nodes."""


def check(edges: list[int], node1: int, node2: int) -> None:
    n = len(edges)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(-1 <= e < n for e in edges), "-1 <= edges[i] < n"
    assert all(e != i for i, e in enumerate(edges)), "edges[i] != i"
    assert 0 <= node1 < n and 0 <= node2 < n, "0 <= node1, node2 < n"
