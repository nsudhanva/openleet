"""Minimum Knight Moves: target coordinates (x, y)."""


def check(x: int, y: int) -> None:
    assert -300 <= x <= 300, "-300 <= x <= 300"
    assert -300 <= y <= 300, "-300 <= y <= 300"
    assert 0 <= abs(x) + abs(y) <= 300, "0 <= |x| + |y| <= 300"
