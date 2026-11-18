"""Restore IP Addresses: a string of digits."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 20, "1 <= s.length <= 20"
    assert all("0" <= c <= "9" for c in s), "s consists of digits only"
