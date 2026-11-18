"""Check if There Is a Valid Parentheses String Path: an m x n grid of '(' and ')'."""


def check(grid: list[list[str]]) -> None:
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(c in ("(", ")") for row in grid for c in row), "grid[i][j] is either '(' or ')'"
