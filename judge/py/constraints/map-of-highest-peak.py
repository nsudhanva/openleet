"""Map of Highest Peak: an m x n grid of 0 (land) and 1 (water) with some water."""


def check(isWater: list[list[int]]) -> None:
    m = len(isWater)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(isWater[0])
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(len(r) == n for r in isWater), "n == isWater[i].length"
    assert all(v in (0, 1) for r in isWater for v in r), "isWater[i][j] is 0 or 1"
    assert any(1 in r for r in isWater), "at least one water cell"
