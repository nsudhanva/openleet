"""Check if Strings Can be Made Equal With Operations II: two lowercase strings of equal length."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(s1: str, s2: str) -> None:
    assert len(s1) == len(s2), "n == s1.length == s2.length"
    assert 1 <= len(s1) <= 10**5, "1 <= n <= 10^5"
    assert set(s1) <= LOWER and set(s2) <= LOWER, (
        "s1 and s2 consist only of lowercase English letters"
    )
