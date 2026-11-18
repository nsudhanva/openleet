"""Zuma Game: a row of colored balls and a hand of colored balls."""


def check(board: str, hand: str) -> None:
    assert isinstance(board, str) and isinstance(hand, str), "board and hand are strings"
    assert 1 <= len(board) <= 16, "1 <= board.length <= 16"
    assert 1 <= len(hand) <= 5, "1 <= hand.length <= 5"
    assert set(board) <= set("RYBGW"), "board consists of 'R', 'Y', 'B', 'G', 'W'"
    assert set(hand) <= set("RYBGW"), "hand consists of 'R', 'Y', 'B', 'G', 'W'"
    run = 1
    for i in range(1, len(board)):
        run = run + 1 if board[i] == board[i - 1] else 1
        assert run < 3, "no initial group of three or more consecutive same-color balls"
