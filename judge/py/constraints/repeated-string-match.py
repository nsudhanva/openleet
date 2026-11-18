"""Repeated String Match: two lowercase strings a and b."""


def check(a: str, b: str) -> None:
    assert isinstance(a, str) and isinstance(b, str), "a and b are strings"
    assert 1 <= len(a) <= 10**4, "1 <= a.length <= 10^4"
    assert 1 <= len(b) <= 10**4, "1 <= b.length <= 10^4"
    assert all("a" <= c <= "z" for c in a + b), "a and b consist of lowercase English letters"
