"""Check If a String Contains All Binary Codes of Size K: a binary string and k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 5 * 10**5, "1 <= s.length <= 5 * 10^5"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
    assert 1 <= k <= 20, "1 <= k <= 20"
