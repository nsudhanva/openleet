"""Check if Number Has Equal Digit Count and Digit Value: a string of digits."""


def check(num: str) -> None:
    assert 1 <= len(num) <= 10, "1 <= n <= 10"
    assert num.isascii() and num.isdigit(), "num consists of digits"
