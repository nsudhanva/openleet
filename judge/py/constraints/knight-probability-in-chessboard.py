"""Knight Probability in Chessboard: board size, moves and the start cell."""


def check(n: int, k: int, row: int, column: int) -> None:
    assert 1 <= n <= 25, "1 <= n <= 25"
    assert 0 <= k <= 100, "0 <= k <= 100"
    assert 0 <= row <= n - 1, "0 <= row <= n - 1"
    assert 0 <= column <= n - 1, "0 <= column <= n - 1"
