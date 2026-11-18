"""Connecting Cities With Minimum Cost: n cities and weighted connections [x, y, cost]."""


def check(n: int, connections: list[list[int]]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= len(connections) <= 10**4, "1 <= connections.length <= 10^4"
    assert all(len(c) == 3 for c in connections), "connections[i].length == 3"
    assert all(1 <= x <= n and 1 <= y <= n for x, y, _ in connections), "1 <= xi, yi <= n"
    assert all(x != y for x, y, _ in connections), "xi != yi"
    assert all(0 <= c <= 10**5 for _, _, c in connections), "0 <= costi <= 10^5"
