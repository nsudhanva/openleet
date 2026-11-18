"""Transform to Chessboard: an n x n binary board."""


def check(board: list[list[int]]) -> None:
    n = len(board)
    assert 2 <= n <= 30, "2 <= n <= 30"
    assert all(len(row) == n for row in board), "n == board.length == board[i].length"
    assert all(v in (0, 1) for row in board for v in row), "board[i][j] is either 0 or 1"
