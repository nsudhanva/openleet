"""Hamming Distance: two non-negative 31-bit integers."""


def check(x: int, y: int) -> None:
    assert 0 <= x <= 2**31 - 1, "0 <= x <= 2^31 - 1"
    assert 0 <= y <= 2**31 - 1, "0 <= y <= 2^31 - 1"
