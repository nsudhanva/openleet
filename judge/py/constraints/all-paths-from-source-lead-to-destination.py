"""All Paths from Source Lead to Destination: n nodes, directed edges, source and destination."""


def check(n: int, edges: list[list[int]], source: int, destination: int) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 0 <= len(edges) <= 10**4, "0 <= edges.length <= 10^4"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= v <= n - 1 for e in edges for v in e), "0 <= ai, bi <= n - 1"
    assert 0 <= source <= n - 1, "0 <= source <= n - 1"
    assert 0 <= destination <= n - 1, "0 <= destination <= n - 1"
