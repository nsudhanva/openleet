"""Split Two Strings to Make Palindrome: two equal-length lowercase strings."""


def check(a: str, b: str) -> None:
    assert isinstance(a, str) and isinstance(b, str), "a and b are strings"
    assert 1 <= len(a) <= 10**5 and 1 <= len(b) <= 10**5, "1 <= a.length, b.length <= 10^5"
    assert len(a) == len(b), "a.length == b.length"
    assert all("a" <= c <= "z" for c in a + b), "a and b consist of lowercase English letters"
