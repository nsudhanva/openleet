"""Rearrange String k Distance Apart: a lowercase string and k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 3 * 10**5, "1 <= s.length <= 3 * 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert 0 <= k <= len(s), "0 <= k <= s.length"
