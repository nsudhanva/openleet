"""Increasing Decreasing String: a string of lowercase letters."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert set(s) <= set("abcdefghijklmnopqrstuvwxyz"), (
        "s consists of only lowercase English letters"
    )
