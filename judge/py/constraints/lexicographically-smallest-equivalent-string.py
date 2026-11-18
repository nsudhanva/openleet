"""Lexicographically Smallest Equivalent String: two equal-length strings and a base string."""


def check(s1: str, s2: str, baseStr: str) -> None:
    assert 1 <= len(s1) <= 1000, "1 <= s1.length <= 1000"
    assert 1 <= len(s2) <= 1000, "1 <= s2.length <= 1000"
    assert 1 <= len(baseStr) <= 1000, "1 <= baseStr.length <= 1000"
    assert len(s1) == len(s2), "s1.length == s2.length"
    for name, t in (("s1", s1), ("s2", s2), ("baseStr", baseStr)):
        assert all("a" <= c <= "z" for c in t), f"{name} consists of lowercase English letters"
