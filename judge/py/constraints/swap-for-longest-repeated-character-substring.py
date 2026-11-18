"""Swap For Longest Repeated Character Substring: a lowercase string."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 2 * 10**4, "1 <= text.length <= 2 * 10^4"
    assert text.isascii() and text.isalpha() and text.islower(), (
        "text consists of lowercase English characters"
    )
