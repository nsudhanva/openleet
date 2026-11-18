"""Valid Number: a short string of letters, digits, '+', '-' and '.'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 20, "1 <= s.length <= 20"
    assert all(c.isascii() and (c.isalnum() or c in "+-.") for c in s), (
        "s consists of English letters, digits, '+', '-' or '.'"
    )
