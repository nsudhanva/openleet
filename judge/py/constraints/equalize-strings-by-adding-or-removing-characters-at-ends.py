"""Equalize Strings by Adding or Removing Characters at Ends: two lowercase strings."""


def check(initial: str, target: str) -> None:
    assert isinstance(initial, str) and isinstance(target, str), "strings"
    assert 1 <= len(initial) <= 1000, "1 <= initial.length <= 1000"
    assert 1 <= len(target) <= 1000, "1 <= target.length <= 1000"
    assert all("a" <= c <= "z" for c in initial + target), "lowercase English letters"
