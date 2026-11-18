"""Check If Digits Are Equal in String After Operations I: a string of digits."""


def check(s: str) -> None:
    assert 3 <= len(s) <= 100, "3 <= s.length <= 100"
    assert s.isascii() and s.isdigit(), "s consists of only digits"
