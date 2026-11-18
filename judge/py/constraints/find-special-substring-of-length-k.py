"""Find Special Substring of Length K: a lowercase string and a length k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= k <= len(s) <= 100, "1 <= k <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters only"
