"""Longest Substring Without Repeating Characters: a string of printable characters."""


def check(s: str) -> None:
    assert 0 <= len(s) <= 10**5, "0 <= s.length <= 10^5"
    assert all(" " <= c <= "~" for c in s), (
        "s consists of English letters, digits, symbols and spaces"
    )
