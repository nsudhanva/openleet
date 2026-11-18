"""Minimum Cost Good Caption: a lowercase string."""


def check(caption: str) -> None:
    assert isinstance(caption, str), "caption is a string"
    assert 1 <= len(caption) <= 5 * 10**4, "1 <= caption.length <= 5 * 10^4"
    assert all("a" <= c <= "z" for c in caption), "caption: lowercase English letters only"
