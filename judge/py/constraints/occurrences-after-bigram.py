"""Occurrences After Bigram: a text of single-space-separated words and two words."""

import re


def check(text: str, first: str, second: str) -> None:
    assert isinstance(text, str), "text is a string"
    assert 1 <= len(text) <= 1000, "1 <= text.length <= 1000"
    assert re.fullmatch(r"[a-z]+( [a-z]+)*", text), (
        "text consists of lowercase letters and single spaces, no leading or trailing spaces"
    )
    for name, w in (("first", first), ("second", second)):
        assert isinstance(w, str), f"{name} is a string"
        assert 1 <= len(w) <= 10, f"1 <= {name}.length <= 10"
        assert re.fullmatch(r"[a-z]+", w), f"{name} consists of lowercase English letters"
