"""Maximum Substrings With Distinct Start: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= ch <= "z" for ch in s), "s consists of lowercase English letters"
