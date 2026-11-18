"""Match Alphanumerical Pattern in Matrix I: a digit board and a pattern of digits and letters."""


def check(board: list[list[int]], pattern: list[str]) -> None:
    assert 1 <= len(board) <= 50, "1 <= board.length <= 50"
    assert all(1 <= len(r) <= 50 for r in board), "1 <= board[i].length <= 50"
    assert all(len(r) == len(board[0]) for r in board), "board is a matrix"
    assert all(0 <= v <= 9 for r in board for v in r), "0 <= board[i][j] <= 9"
    assert 1 <= len(pattern) <= 50, "1 <= pattern.length <= 50"
    assert all(isinstance(p, str) and 1 <= len(p) <= 50 for p in pattern), (
        "1 <= pattern[i].length <= 50"
    )
    assert all(len(p) == len(pattern[0]) for p in pattern), "pattern is a matrix"
    assert all(c in "0123456789" or "a" <= c <= "z" for p in pattern for c in p), (
        "pattern[i][j] is a digit or a lowercase letter"
    )
