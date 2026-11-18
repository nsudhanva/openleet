"""HTML Entity Parser: a string of 8-bit ASCII characters."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 10**5, "1 <= text.length <= 10^5"
    assert all(ord(c) < 256 for c in text), "text contains only the 256 ASCII characters"
