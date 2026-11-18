"""Integer Replacement: a positive 32-bit integer n."""


def check(n: int) -> None:
    assert 1 <= n <= 2**31 - 1, "1 <= n <= 2^31 - 1"
