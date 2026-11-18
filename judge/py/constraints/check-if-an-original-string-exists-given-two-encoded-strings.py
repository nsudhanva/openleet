"""Check if an Original String Exists Given Two Encoded Strings: two encoded strings."""

import re


def check(s1: str, s2: str) -> None:
    assert isinstance(s1, str) and isinstance(s2, str), "s1, s2 are strings"
    assert 1 <= len(s1) <= 40, "1 <= s1.length <= 40"
    assert 1 <= len(s2) <= 40, "1 <= s2.length <= 40"
    for s in (s1, s2):
        assert all(c in "123456789" or "a" <= c <= "z" for c in s), (
            "s consists of digits 1-9 and lowercase English letters only"
        )
        assert not re.search(r"[1-9]{4}", s), "at most 3 consecutive digits"
