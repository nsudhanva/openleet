"""Nearest Exit from Entrance in Maze: an m x n grid of '.' and '+' and an entrance cell."""


def check(maze: list[list[str]], entrance: list[int]) -> None:
    m = len(maze)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(maze[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in maze), "maze[i].length == n"
    assert all(c in (".", "+") for row in maze for c in row), "maze[i][j] is either '.' or '+'"
    assert len(entrance) == 2, "entrance.length == 2"
    assert 0 <= entrance[0] < m, "0 <= entrance_row < m"
    assert 0 <= entrance[1] < n, "0 <= entrance_col < n"
    assert maze[entrance[0]][entrance[1]] == ".", "entrance will always be an empty cell"
