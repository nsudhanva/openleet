"""Valid Sudoku: a 9 x 9 board of digits '1'-'9' or '.'."""


def check(board: list[list[str]]) -> None:
    assert len(board) == 9, "board.length == 9"
    assert all(len(row) == 9 for row in board), "board[i].length == 9"
    assert all(c in set("123456789.") and len(c) == 1 for row in board for c in row), (
        "board[i][j] is a digit 1-9 or '.'"
    )
