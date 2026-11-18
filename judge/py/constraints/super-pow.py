"""Super Pow: a base a and a huge exponent given as a digit list."""


def check(a: int, b: list[int]) -> None:
    assert 1 <= a <= 2**31 - 1, "1 <= a <= 2^31 - 1"
    assert 1 <= len(b) <= 2000, "1 <= b.length <= 2000"
    assert all(0 <= d <= 9 for d in b), "0 <= b[i] <= 9"
    assert b[0] != 0 or len(b) == 1, "b does not contain leading zeros"
