"""Find the City With the Smallest Number of Neighbors: n, weighted edges, threshold."""


def check(n: int, edges: list[list[int]], distanceThreshold: int) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert isinstance(edges, list), "edges is an array"
    assert 1 <= len(edges) <= n * (n - 1) // 2, "1 <= edges.length <= n * (n - 1) / 2"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= a < b < n for a, b, _ in edges), "0 <= fromi < toi < n"
    assert all(1 <= w <= 10**4 for _, _, w in edges), "1 <= weighti <= 10^4"
    assert 1 <= distanceThreshold <= 10**4, "1 <= distanceThreshold <= 10^4"
    assert len({(a, b) for a, b, _ in edges}) == len(edges), "all pairs (fromi, toi) are distinct"
