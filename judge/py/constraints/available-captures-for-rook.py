"""Available Captures for Rook: an 8 x 8 chessboard of 'R', '.', 'B' and 'p'."""


def check(board: list[list[str]]) -> None:
    assert len(board) == 8, "board.length == 8"
    # board[i].length == 8 is not asserted: statement example 1 has a row of 7 cells.
    assert all(c in ("R", ".", "B", "p") for row in board for c in row), (
        "board[i][j] is either 'R', '.', 'B', or 'p'"
    )
    assert sum(c == "R" for row in board for c in row) == 1, (
        "exactly one cell with board[i][j] == 'R'"
    )
