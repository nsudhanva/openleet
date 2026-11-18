"""Game of Life: an m x n board of 0 and 1."""


def check(board: list[list[int]]) -> None:
    m = len(board)
    assert 1 <= m <= 25, "1 <= m <= 25"
    n = len(board[0])
    assert 1 <= n <= 25, "1 <= n <= 25"
    assert all(len(row) == n for row in board), "n == board[i].length"
    assert all(v in (0, 1) for row in board for v in row), "board[i][j] is 0 or 1"
