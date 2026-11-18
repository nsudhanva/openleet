"""Number of Paths with Max Score: a square board of 'E', 'S', 'X' and digits 1-9."""


def check(board: list[str]) -> None:
    n = len(board)
    assert 2 <= n <= 100, "2 <= board.length <= 100"
    assert all(len(row) == n for row in board), "board.length == board[i].length"
    assert board[0][0] == "E", "top left square is 'E'"
    assert board[n - 1][n - 1] == "S", "bottom right square is 'S'"
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if (i, j) in ((0, 0), (n - 1, n - 1)):
                continue
            assert c == "X" or "1" <= c <= "9", "other squares are digits 1-9 or 'X'"
