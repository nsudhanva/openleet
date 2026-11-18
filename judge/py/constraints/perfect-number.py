"""Perfect Number: one integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert 1 <= num <= 10**8, "1 <= num <= 10^8"
