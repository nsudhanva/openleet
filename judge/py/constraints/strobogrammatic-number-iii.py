"""Strobogrammatic Number III: low and high digit strings."""


def check(low: str, high: str) -> None:
    assert isinstance(low, str) and isinstance(high, str), "low and high are strings"
    assert 1 <= len(low) <= 15 and 1 <= len(high) <= 15, "1 <= low.length, high.length <= 15"
    assert low.isascii() and low.isdigit() and high.isascii() and high.isdigit(), (
        "low and high consist of only digits"
    )
    assert int(low) <= int(high), "low <= high"
    for s in (low, high):
        assert s == "0" or s[0] != "0", "no leading zeros except for zero itself"
