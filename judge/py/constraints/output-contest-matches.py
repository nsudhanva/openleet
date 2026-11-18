"""Output Contest Matches: the number of teams n, a power of two."""


def check(n: int) -> None:
    assert isinstance(n, int) and n > 0, "n is a positive integer"
    assert n & (n - 1) == 0, "n == 2^x"
    assert 1 <= n.bit_length() - 1 <= 12, "x in the range [1, 12]"
