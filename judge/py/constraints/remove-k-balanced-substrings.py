"""Remove K-Balanced Substrings: a parentheses string and k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 10**5, "2 <= s.length <= 10^5"
    assert all(c in "()" for c in s), "s consists only of '(' and ')'"
    assert isinstance(k, int), "k is an integer"
    assert k >= 1 and 2 * k <= len(s), "1 <= k <= s.length / 2"
