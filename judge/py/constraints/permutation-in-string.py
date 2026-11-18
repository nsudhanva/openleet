"""Permutation in String: two lowercase strings."""

import re


def check(s1: str, s2: str) -> None:
    assert isinstance(s1, str) and isinstance(s2, str), "s1 and s2 are strings"
    assert 1 <= len(s1) <= 10**4, "1 <= s1.length <= 10^4"
    assert 1 <= len(s2) <= 10**4, "1 <= s2.length <= 10^4"
    assert re.fullmatch(r"[a-z]+", s1) and re.fullmatch(r"[a-z]+", s2), (
        "s1 and s2 consist of lowercase English letters"
    )
