"""To Lower Case: a string of printable ASCII characters."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(32 <= ord(c) <= 126 for c in s), "s consists of printable ASCII characters"
