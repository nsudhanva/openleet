"""Check If Digits Are Equal in String After Operations II: a string of digits."""


def check(s: str) -> None:
    assert 3 <= len(s) <= 10**5, "3 <= s.length <= 10^5"
    assert s.isascii() and s.isdigit(), "s consists of only digits"
