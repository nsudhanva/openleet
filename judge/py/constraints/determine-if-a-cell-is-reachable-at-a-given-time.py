"""Determine if a Cell Is Reachable at a Given Time: start, finish and time."""


def check(sx: int, sy: int, fx: int, fy: int, t: int) -> None:
    assert all(1 <= v <= 10**9 for v in (sx, sy, fx, fy)), "1 <= sx, sy, fx, fy <= 10^9"
    assert 0 <= t <= 10**9, "0 <= t <= 10^9"
