"""Flower Planting With No Adjacent: n gardens and bidirectional paths, degree at most 3."""


def check(n: int, paths: list[list[int]]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 0 <= len(paths) <= 2 * 10**4, "0 <= paths.length <= 2 * 10^4"
    assert all(len(p) == 2 for p in paths), "paths[i].length == 2"
    assert all(1 <= x <= n and 1 <= y <= n for x, y in paths), "1 <= xi, yi <= n"
    assert all(x != y for x, y in paths), "xi != yi"
    deg = [0] * (n + 1)
    for x, y in paths:
        deg[x] += 1
        deg[y] += 1
    assert max(deg) <= 3, "every garden has at most 3 paths"
