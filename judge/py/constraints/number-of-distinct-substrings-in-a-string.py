"""Number of Distinct Substrings in a String: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
