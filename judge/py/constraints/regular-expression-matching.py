"""Regular Expression Matching: a lowercase string s and a pattern p of letters, '.' and '*'."""


def check(s: str, p: str) -> None:
    assert 1 <= len(s) <= 20, "1 <= s.length <= 20"
    assert 1 <= len(p) <= 20, "1 <= p.length <= 20"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
    assert all("a" <= c <= "z" or c in ".*" for c in p), (
        "p contains only lowercase English letters, '.', and '*'"
    )
    assert all(c != "*" or (i > 0 and p[i - 1] != "*") for i, c in enumerate(p)), (
        "each '*' has a previous valid character to match"
    )
