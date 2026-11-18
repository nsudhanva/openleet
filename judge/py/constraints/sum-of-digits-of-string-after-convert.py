"""Sum of Digits of String After Convert: a lowercase string and a repeat count k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 1 <= k <= 10, "1 <= k <= 10"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
