"""Candy Crush: an m x n board of candy types, 0 for empty."""


def check(board: list[list[int]]) -> None:
    m = len(board)
    assert 3 <= m <= 50, "3 <= m <= 50"
    n = len(board[0])
    assert 3 <= n <= 50, "3 <= n <= 50"
    assert all(len(r) == n for r in board), "n == board[i].length"
    # the statement itself uses 0 for an empty cell, so 0 is allowed alongside 1..2000
    assert all(0 <= v <= 2000 for r in board for v in r), "board[i][j] <= 2000 (0 = empty)"
