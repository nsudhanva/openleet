"""Count K-Subsequences of a String With Maximum Beauty: a lowercase string and k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2 * 10**5, "1 <= s.length <= 2 * 10^5"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
