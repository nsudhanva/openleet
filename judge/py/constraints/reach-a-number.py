"""Reach a Number: a nonzero target on the number line."""


def check(target: int) -> None:
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
    assert target != 0, "target != 0"
