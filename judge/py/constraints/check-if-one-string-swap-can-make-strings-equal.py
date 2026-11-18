"""Check if One String Swap Can Make Strings Equal: two lowercase strings of equal length."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(s1: str, s2: str) -> None:
    assert 1 <= len(s1) <= 100 and 1 <= len(s2) <= 100, "1 <= s1.length, s2.length <= 100"
    assert len(s1) == len(s2), "s1.length == s2.length"
    assert set(s1) <= LOWER and set(s2) <= LOWER, (
        "s1 and s2 consist of only lowercase English letters"
    )
