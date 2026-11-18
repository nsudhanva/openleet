"""Rotating the Box: an m x n grid of '#', '*' and '.'."""


def check(boxGrid: list[list[str]]) -> None:
    m = len(boxGrid)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(boxGrid[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(r) == n for r in boxGrid), "n == boxGrid[i].length"
    assert all(c in ("#", "*", ".") for r in boxGrid for c in r), (
        "boxGrid[i][j] is either '#', '*', or '.'"
    )
