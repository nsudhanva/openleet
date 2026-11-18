"""Lexicographically Smallest Beautiful String: a beautiful string over the first k letters."""


def check(s: str, k: int) -> None:
    n = len(s)
    assert 1 <= n <= 10**5, "1 <= n == s.length <= 10^5"
    assert 4 <= k <= 26, "4 <= k <= 26"
    assert all("a" <= c < chr(ord("a") + k) for c in s), "s uses only the first k letters"
    assert all(s[i] != s[i + 1] for i in range(n - 1)), "s has no palindrome of length 2"
    assert all(s[i] != s[i + 2] for i in range(n - 2)), "s has no palindrome of length 3"
