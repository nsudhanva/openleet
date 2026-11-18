"""String to Integer (atoi): a string of letters, digits, spaces, signs and dots."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 0 <= len(s) <= 200, "0 <= s.length <= 200"
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-.")
    assert all(c in allowed for c in s), "s consists of letters, digits, ' ', '+', '-', and '.'"
