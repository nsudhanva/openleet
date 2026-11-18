"""Dungeon Game: an m x n grid of health changes."""


def check(dungeon: list[list[int]]) -> None:
    m = len(dungeon)
    assert 1 <= m <= 200, "1 <= m <= 200"
    assert all(isinstance(row, list) for row in dungeon), "dungeon is a list of rows"
    n = len(dungeon[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in dungeon), "n == dungeon[i].length"
    assert all(isinstance(v, int) and -1000 <= v <= 1000 for row in dungeon for v in row), (
        "-1000 <= dungeon[i][j] <= 1000"
    )
