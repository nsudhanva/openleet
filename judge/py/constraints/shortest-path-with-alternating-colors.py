"""Shortest Path with Alternating Colors: n nodes with red and blue directed edge lists."""


def check(n: int, redEdges: list[list[int]], blueEdges: list[list[int]]) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 0 <= len(redEdges) <= 400, "0 <= redEdges.length <= 400"
    assert 0 <= len(blueEdges) <= 400, "0 <= blueEdges.length <= 400"
    assert all(len(e) == 2 for e in redEdges), "redEdges[i].length == 2"
    assert all(len(e) == 2 for e in blueEdges), "blueEdges[j].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in redEdges), "0 <= ai, bi < n"
    assert all(0 <= u < n and 0 <= v < n for u, v in blueEdges), "0 <= uj, vj < n"
