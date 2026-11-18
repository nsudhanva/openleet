"""Binary Number with Alternating Bits: one positive integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 2**31 - 1, "1 <= n <= 2^31 - 1"
