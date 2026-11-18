"""Happy Number: a positive 31-bit integer."""


def check(n: int) -> None:
    assert 1 <= n <= 2**31 - 1, "1 <= n <= 2^31 - 1"
