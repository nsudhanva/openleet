"""Remove K Digits: a non-negative integer as a digit string and k."""


def check(num: str, k: int) -> None:
    assert isinstance(num, str), "num is a string"
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= len(num) <= 10**5, "1 <= k <= num.length <= 10^5"
    assert num.isascii() and num.isdigit(), "num consists of only digits"
    assert num == "0" or num[0] != "0", "num has no leading zeros except zero itself"
