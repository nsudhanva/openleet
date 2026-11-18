"""Find Center of Star Graph: the n - 1 edges of a star on nodes 1..n."""

from collections import Counter


def check(edges: list[list[int]]) -> None:
    n = len(edges) + 1
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= x <= n for e in edges for x in e), "1 <= ui, vi <= n"
    assert all(e[0] != e[1] for e in edges), "ui != vi"
    deg = Counter(x for e in edges for x in e)
    centers = [v for v, d in deg.items() if d == n - 1]
    assert len(centers) == 1, "the edges represent a valid star graph"
    assert all(centers[0] in e for e in edges), "every edge touches the center"
    assert len(deg) == n, "every node 1..n is in the star"
