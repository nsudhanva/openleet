"""Maximum Score From Removing Substrings: a lowercase string and two positive gains."""


def check(s: str, x: int, y: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= ch <= "z" for ch in s), "s consists of lowercase English letters"
    assert 1 <= x <= 10**4 and 1 <= y <= 10**4, "1 <= x, y <= 10^4"
