"""Count Sub Islands: two binary grids of the same shape."""


def check(grid1: list[list[int]], grid2: list[list[int]]) -> None:
    m = len(grid1)
    assert 1 <= m <= 500, "1 <= m <= 500"
    assert len(grid2) == m, "m == grid1.length == grid2.length"
    n = len(grid1[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(r) == n for r in grid1), "n == grid1[i].length"
    assert all(len(r) == n for r in grid2), "n == grid2[i].length"
    assert all(v in (0, 1) for r in grid1 for v in r), "grid1[i][j] is 0 or 1"
    assert all(v in (0, 1) for r in grid2 for v in r), "grid2[i][j] is 0 or 1"
