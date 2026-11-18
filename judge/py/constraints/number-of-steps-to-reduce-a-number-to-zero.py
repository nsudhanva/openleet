"""Number of Steps to Reduce a Number to Zero: one integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert 0 <= num <= 10**6, "0 <= num <= 10^6"
