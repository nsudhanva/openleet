"""Divide a String Into Groups of Size k: a lowercase string, group size and fill letter."""


def check(s: str, k: int, fill: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters only"
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert len(fill) == 1 and "a" <= fill <= "z", "fill is a lowercase English letter"
