"""The Maze III: a 0/1 grid with a ball and a hole on empty cells."""


def check(maze: list[list[int]], ball: list[int], hole: list[int]) -> None:
    m = len(maze)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(maze[0])
    assert all(len(row) == n for row in maze), "n == maze[i].length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(v in (0, 1) for row in maze for v in row), "maze[i][j] is 0 or 1"
    assert len(ball) == 2, "ball.length == 2"
    assert len(hole) == 2, "hole.length == 2"
    assert 0 <= ball[0] < m and 0 <= hole[0] < m, "ballrow, holerow inside the maze"
    assert 0 <= ball[1] < n and 0 <= hole[1] < n, "ballcol, holecol inside the maze"
    assert maze[ball[0]][ball[1]] == 0, "the ball is in an empty space"
    assert maze[hole[0]][hole[1]] == 0, "the hole is in an empty space"
    assert ball != hole, "ball and hole are not in the same position"
    assert sum(v == 0 for row in maze for v in row) >= 2, (
        "the maze contains at least 2 empty spaces"
    )
