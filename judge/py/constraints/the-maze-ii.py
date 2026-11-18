"""The Maze II: a 0/1 grid with a start and a destination on empty cells."""


def check(maze: list[list[int]], start: list[int], destination: list[int]) -> None:
    m = len(maze)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(maze[0])
    assert all(len(row) == n for row in maze), "n == maze[i].length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(v in (0, 1) for row in maze for v in row), "maze[i][j] is 0 or 1"
    assert len(start) == 2, "start.length == 2"
    assert len(destination) == 2, "destination.length == 2"
    assert 0 <= start[0] < m and 0 <= destination[0] < m, "0 <= startrow, destinationrow < m"
    assert 0 <= start[1] < n and 0 <= destination[1] < n, "0 <= startcol, destinationcol < n"
    assert maze[start[0]][start[1]] == 0, "the ball is in an empty space"
    assert maze[destination[0]][destination[1]] == 0, "the destination is in an empty space"
    assert start != destination, "ball and destination are not in the same position"
    assert sum(v == 0 for row in maze for v in row) >= 2, (
        "the maze contains at least 2 empty spaces"
    )
