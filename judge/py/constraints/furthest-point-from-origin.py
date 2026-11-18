"""Furthest Point From Origin: a string of moves 'L', 'R' and '_'."""


def check(moves: str) -> None:
    assert 1 <= len(moves) <= 50, "1 <= moves.length == n <= 50"
    assert set(moves) <= set("LR_"), "moves consists only of 'L', 'R' and '_'"
