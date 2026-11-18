"""Number of Changing Keys: a string of English letters."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c.isascii() and c.isalpha() for c in s), (
        "s consists of only upper case and lower case English letters"
    )
