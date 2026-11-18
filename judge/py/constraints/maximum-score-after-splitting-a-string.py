"""Maximum Score After Splitting a String: a binary string."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 500, "2 <= s.length <= 500"
    assert all(c in "01" for c in s), "s consists of characters '0' and '1' only"
