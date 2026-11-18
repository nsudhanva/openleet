"""Backspace String Compare: two strings of lowercase letters and '#'."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 200 and 1 <= len(t) <= 200, "1 <= s.length, t.length <= 200"
    ok = set("abcdefghijklmnopqrstuvwxyz#")
    assert set(s) <= ok and set(t) <= ok, (
        "s and t only contain lowercase letters and '#' characters"
    )
