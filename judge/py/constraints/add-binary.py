"""Add Binary: two binary strings without leading zeros."""


def check(a: str, b: str) -> None:
    for s in (a, b):
        assert 1 <= len(s) <= 10**4, "1 <= a.length, b.length <= 10^4"
        assert set(s) <= {"0", "1"}, "a and b consist only of '0' or '1' characters"
        assert s == "0" or s[0] != "0", "no leading zeros except for the zero itself"
