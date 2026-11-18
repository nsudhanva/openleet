"""Maximum Bitwise XOR After Rearrangement: two equal-length binary strings."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 2 * 10**5, "1 <= n <= 2 * 10^5"
    assert len(s) == len(t), "s.length == t.length"
    assert set(s) <= {"0", "1"}, "s[i] is '0' or '1'"
    assert set(t) <= {"0", "1"}, "t[i] is '0' or '1'"
