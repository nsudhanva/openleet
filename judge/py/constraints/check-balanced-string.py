"""Check Balanced String: a string of digits."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 2 <= len(num) <= 100, "2 <= num.length <= 100"
    assert all("0" <= c <= "9" for c in num), "num consists of digits only"
