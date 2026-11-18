"""Count Unique Characters of All Substrings of a Given String: an uppercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("A" <= c <= "Z" for c in s), "s consists of uppercase English letters only"
