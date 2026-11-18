"""Excel Sheet Column Title: a column number."""


def check(columnNumber: int) -> None:
    assert 1 <= columnNumber <= 2**31 - 1, "1 <= columnNumber <= 2^31 - 1"
