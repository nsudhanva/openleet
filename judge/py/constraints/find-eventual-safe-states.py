"""Find Eventual Safe States: a directed graph as adjacency lists (self-loops allowed)."""

from itertools import pairwise


def check(graph: list[list[int]]) -> None:
    n = len(graph)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(0 <= len(g) <= n for g in graph), "0 <= graph[i].length <= n"
    assert all(0 <= x <= n - 1 for g in graph for x in g), "0 <= graph[i][j] <= n - 1"
    assert all(a < b for g in graph for a, b in pairwise(g)), (
        "graph[i] is sorted in strictly increasing order"
    )
    assert 1 <= sum(len(g) for g in graph) <= 4 * 10**4, "the number of edges is in [1, 4 * 10^4]"
