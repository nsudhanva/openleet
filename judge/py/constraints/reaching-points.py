"""Reaching Points: start (sx, sy) and target (tx, ty)."""


def check(sx: int, sy: int, tx: int, ty: int) -> None:
    assert all(1 <= v <= 10**9 for v in (sx, sy, tx, ty)), "1 <= sx, sy, tx, ty <= 10^9"
