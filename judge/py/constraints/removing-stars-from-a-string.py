"""Removing Stars From a String: lowercase letters and stars, each star removable."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c == "*" or "a" <= c <= "z" for c in s), (
        "s consists of lowercase English letters and stars"
    )
    letters = 0
    for c in s:
        if c == "*":
            letters -= 1
            assert letters >= 0, "the star operation can be performed on s"
        else:
            letters += 1
