"""Digit Count in Range: a digit and an inclusive range."""


def check(d: int, low: int, high: int) -> None:
    assert 0 <= d <= 9, "0 <= d <= 9"
    assert 1 <= low <= high <= 2 * 10**8, "1 <= low <= high <= 2 * 10^8"
