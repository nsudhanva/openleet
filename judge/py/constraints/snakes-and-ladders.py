"""Snakes and Ladders: an n x n board of -1 or destination labels."""


def check(board: list[list[int]]) -> None:
    n = len(board)
    assert 2 <= n <= 20, "2 <= n <= 20"
    assert all(len(r) == n for r in board), "n == board.length == board[i].length"
    assert all(isinstance(v, int) and (v == -1 or 1 <= v <= n * n) for r in board for v in r), (
        "board[i][j] is either -1 or in the range [1, n^2]"
    )

    def cell(label: int) -> int:
        r, c = divmod(label - 1, n)
        if r % 2:
            c = n - 1 - c
        return board[n - 1 - r][c]

    assert cell(1) == -1, "square 1 is not the start of a snake or ladder"
    assert cell(n * n) == -1, "square n^2 is not the start of a snake or ladder"
