"""Minimum Suffix Flips: a binary string."""


def check(target: str) -> None:
    assert 1 <= len(target) <= 10**5, "1 <= n <= 10^5"
    assert set(target) <= {"0", "1"}, "target[i] is either '0' or '1'"
