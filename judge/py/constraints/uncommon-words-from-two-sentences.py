"""Uncommon Words from Two Sentences: two sentences of lowercase words."""


def check(s1: str, s2: str) -> None:
    for s in (s1, s2):
        assert 1 <= len(s) <= 200, "1 <= s1.length, s2.length <= 200"
        assert all(c == " " or "a" <= c <= "z" for c in s), "lowercase English letters and spaces"
        assert not s.startswith(" ") and not s.endswith(" "), "no leading or trailing spaces"
        assert "  " not in s, "words are separated by a single space"
