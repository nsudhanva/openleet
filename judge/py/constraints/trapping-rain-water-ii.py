"""Trapping Rain Water II: an m x n height map."""


def check(heightMap: list[list[int]]) -> None:
    m = len(heightMap)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(heightMap[0])
    assert all(len(r) == n for r in heightMap), "n == heightMap[i].length"
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(0 <= v <= 2 * 10**4 for r in heightMap for v in r), (
        "0 <= heightMap[i][j] <= 2 * 10^4"
    )
