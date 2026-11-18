"""Number Complement: a positive integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert 1 <= num < 2**31, "1 <= num < 2^31"
