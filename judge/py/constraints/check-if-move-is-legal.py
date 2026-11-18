"""Check if Move is Legal: an 8 x 8 board of '.', 'B', 'W', a move cell and a color."""


def check(board: list[list[str]], rMove: int, cMove: int, color: str) -> None:
    assert len(board) == 8, "board.length == 8"
    assert all(len(row) == 8 for row in board), "board[r].length == 8"
    assert all(c in (".", "B", "W") for row in board for c in row), (
        "board cells are '.', 'B' or 'W'"
    )
    assert 0 <= rMove < 8 and 0 <= cMove < 8, "0 <= rMove, cMove < 8"
    assert board[rMove][cMove] == ".", "board[rMove][cMove] == '.'"
    assert color in ("B", "W"), "color is either 'B' or 'W'"
