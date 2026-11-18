"""Rearrange Characters to Make Target String: two lowercase strings."""


def check(s: str, target: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 1 <= len(target) <= 10, "1 <= target.length <= 10"
    for t in (s, target):
        assert all("a" <= c <= "z" for c in t), "lowercase English letters"
