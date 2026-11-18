"""Split Array into Fibonacci Sequence: a string of digits."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 1 <= len(num) <= 200, "1 <= num.length <= 200"
    assert all("0" <= c <= "9" for c in num), "num contains only digits"
