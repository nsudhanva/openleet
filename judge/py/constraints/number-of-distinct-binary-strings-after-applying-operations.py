"""Number of Distinct Binary Strings After Applying Operations: a binary string and a flip size."""


def check(s: str, k: int) -> None:
    assert 1 <= k <= len(s) <= 10**5, "1 <= k <= s.length <= 10^5"
    assert all(c in "01" for c in s), "s[i] is either 0 or 1"
