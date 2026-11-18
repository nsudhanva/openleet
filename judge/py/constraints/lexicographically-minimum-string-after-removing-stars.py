"""Lexicographically Minimum String After Removing Stars: lowercase letters and '*'."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c == "*" or "a" <= c <= "z" for c in s), (
        "s consists only of lowercase English letters and '*'"
    )
    letters = 0
    for c in s:
        if c == "*":
            letters -= 1
            assert letters >= 0, "it is possible to delete all '*' characters"
        else:
            letters += 1
