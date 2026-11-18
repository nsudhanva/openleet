"""Surrounded Regions: an m x n board of 'X' and 'O' characters."""


def check(board: list[list[str]]) -> None:
    m = len(board)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(board[0]) if board else 0
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in board), "n == board[i].length"
    assert all(c in ("X", "O") for row in board for c in row), "board[i][j] is 'X' or 'O'"
