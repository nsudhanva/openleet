"""K-Similar Strings: two anagram strings over the letters a to f."""


def check(s1: str, s2: str) -> None:
    assert 1 <= len(s1) <= 20, "1 <= s1.length <= 20"
    assert len(s2) == len(s1), "s2.length == s1.length"
    assert set(s1 + s2) <= set("abcdef"), "only letters a-f"
    assert sorted(s1) == sorted(s2), "s2 is an anagram of s1"
