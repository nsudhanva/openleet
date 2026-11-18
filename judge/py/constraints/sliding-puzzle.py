"""Sliding Puzzle: a 2 x 3 board holding 0..5 once each."""


def check(board: list[list[int]]) -> None:
    assert len(board) == 2, "board.length == 2"
    assert all(len(row) == 3 for row in board), "board[i].length == 3"
    values = [v for row in board for v in row]
    assert all(0 <= v <= 5 for v in values), "0 <= board[i][j] <= 5"
    assert len(set(values)) == 6, "each value board[i][j] is unique"
