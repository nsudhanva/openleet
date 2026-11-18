"""Longest Repeating Character Replacement: an uppercase string and a replacement budget k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("A" <= c <= "Z" for c in s), "s consists of only uppercase English letters"
    assert 0 <= k <= len(s), "0 <= k <= s.length"
