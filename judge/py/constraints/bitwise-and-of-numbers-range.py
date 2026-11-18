"""Bitwise AND of Numbers Range: an inclusive range of non-negative integers."""


def check(left: int, right: int) -> None:
    assert 0 <= left <= right <= 2**31 - 1, "0 <= left <= right <= 2^31 - 1"
