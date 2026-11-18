"""Minimum Deletions for at Most K Distinct Characters: a short lowercase string and k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 16, "1 <= s.length <= 16"
    assert 1 <= k <= 16, "1 <= k <= 16"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
