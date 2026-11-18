"""Check if Strings Can be Made Equal With Operations I: two lowercase strings of length 4."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(s1: str, s2: str) -> None:
    assert len(s1) == len(s2) == 4, "s1.length == s2.length == 4"
    assert set(s1) <= LOWER and set(s2) <= LOWER, (
        "s1 and s2 consist only of lowercase English letters"
    )
