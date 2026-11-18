"""Maximum Number of Vowels in a Substring of Given Length: a lowercase string and a window."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
