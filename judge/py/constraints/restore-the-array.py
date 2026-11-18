"""Restore The Array: a digit string without leading zeros and an upper bound k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("0" <= c <= "9" for c in s), "s consists of only digits"
    assert s[0] != "0", "s does not contain leading zeros"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
