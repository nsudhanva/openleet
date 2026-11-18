"""Divide Nodes Into the Maximum Number of Groups: an undirected graph on nodes 1..n."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert 1 <= len(edges) <= 10**4, "1 <= edges.length <= 10^4"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in edges), "1 <= ai, bi <= n"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), (
        "at most one edge between any pair"
    )
