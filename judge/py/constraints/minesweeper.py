"""Minesweeper: a board of 'M', 'E', 'B' and digit cells, and a click position."""


def check(board: list[list[str]], click: list[int]) -> None:
    m = len(board)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(board[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(r) == n for r in board), "n == board[i].length"
    allowed = set("MEB12345678")
    assert all(c in allowed for r in board for c in r), "board[i][j] is 'M', 'E', 'B' or '1'-'8'"
    assert len(click) == 2, "click.length == 2"
    assert 0 <= click[0] < m, "0 <= clickr < m"
    assert 0 <= click[1] < n, "0 <= clickc < n"
    assert board[click[0]][click[1]] in ("M", "E"), "board[clickr][clickc] is 'M' or 'E'"
