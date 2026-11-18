"""Shortest Way to Form String: two lowercase strings."""


def check(source: str, target: str) -> None:
    assert 1 <= len(source) <= 1000, "1 <= source.length <= 1000"
    assert 1 <= len(target) <= 1000, "1 <= target.length <= 1000"
    letters = set("abcdefghijklmnopqrstuvwxyz")
    assert set(source) <= letters, "source consists of lowercase English letters"
    assert set(target) <= letters, "target consists of lowercase English letters"
