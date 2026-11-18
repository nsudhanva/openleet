"""Maximum Number of Non-overlapping Palindrome Substrings: a lowercase string and a minimum
length k."""


def check(s: str, k: int) -> None:
    assert 1 <= k <= len(s) <= 2000, "1 <= k <= s.length <= 2000"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
