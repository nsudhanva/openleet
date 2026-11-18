"""Select K Disjoint Special Substrings: a lowercase string and an integer k."""

import string


def check(s: str, k: int) -> None:
    assert isinstance(s, str) and 2 <= len(s) <= 5 * 10**4, "2 <= n == s.length <= 5 * 10^4"
    assert 0 <= k <= 26, "0 <= k <= 26"
    assert set(s) <= set(string.ascii_lowercase), "s consists only of lowercase English letters"
