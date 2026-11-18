"""Valid Perfect Square: a positive 32-bit integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert 1 <= num <= 2**31 - 1, "1 <= num <= 2^31 - 1"
