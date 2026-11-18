"""Find K-Length Substrings With No Repeated Characters: a lowercase string and a length k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), (
        "s consists of lowercase English letters"
    )
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
