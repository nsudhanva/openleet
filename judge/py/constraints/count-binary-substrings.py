"""Count Binary Substrings: a binary string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in ("0", "1") for c in s), "s[i] is '0' or '1'"
