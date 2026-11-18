"""Binary String With Substrings Representing 1 To N: a binary string and n."""


def check(s: str, n: int) -> None:
    assert isinstance(s, str) and isinstance(n, int), "s is a string and n an integer"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
