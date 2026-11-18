"""Minimum String Length After Removing Substrings: a short uppercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("A" <= c <= "Z" and len(c) == 1 for c in s), (
        "s consists only of uppercase English letters"
    )
