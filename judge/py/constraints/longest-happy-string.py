"""Longest Happy String: three letter counts a, b, c."""


def check(a: int, b: int, c: int) -> None:
    assert 0 <= a <= 100, "0 <= a <= 100"
    assert 0 <= b <= 100, "0 <= b <= 100"
    assert 0 <= c <= 100, "0 <= c <= 100"
    assert a + b + c > 0, "a + b + c > 0"
