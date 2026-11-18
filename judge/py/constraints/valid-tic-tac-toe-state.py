"""Valid Tic-Tac-Toe State: a 3 x 3 board as three 3-character strings."""


def check(board: list[str]) -> None:
    assert len(board) == 3, "board.length == 3"
    assert all(len(row) == 3 for row in board), "board[i].length == 3"
    assert all(c in "XO " for row in board for c in row), "board[i][j] is either 'X', 'O', or ' '"
