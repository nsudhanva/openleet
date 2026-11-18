"""Lexicographically Smallest Palindromic Permutation Greater Than Target: two equal-length
lowercase strings."""


def check(s: str, target: str) -> None:
    assert isinstance(s, str) and isinstance(target, str), "s and target are strings"
    assert 1 <= len(s) <= 300, "1 <= n <= 300"
    assert len(s) == len(target), "s.length == target.length"
    assert all("a" <= c <= "z" for c in s + target), (
        "s and target consist of only lowercase English letters"
    )
