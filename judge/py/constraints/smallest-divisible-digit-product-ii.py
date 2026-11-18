"""Smallest Divisible Digit Product II: a digit string and an integer t."""


def check(num: str, t: int) -> None:
    assert 2 <= len(num) <= 2 * 10**5, "2 <= num.length <= 2 * 10^5"
    assert num.isascii() and num.isdigit(), "num consists only of digits"
    assert num[0] != "0", "num does not contain leading zeros"
    assert 1 <= t <= 10**14, "1 <= t <= 10^14"
