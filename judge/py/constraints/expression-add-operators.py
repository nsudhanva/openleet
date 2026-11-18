"""Expression Add Operators: a digit string and an integer target."""


def check(num: str, target: int) -> None:
    assert isinstance(num, str), "num is a string"
    assert 1 <= len(num) <= 10, "1 <= num.length <= 10"
    assert num.isascii() and num.isdigit(), "num consists of only digits"
    assert -(2**31) <= target <= 2**31 - 1, "-2^31 <= target <= 2^31 - 1"
