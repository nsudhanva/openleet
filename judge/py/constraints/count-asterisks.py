"""Count Asterisks: a string of lowercase letters, '|' and '*'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(("a" <= c <= "z") or c in "|*" for c in s), (
        "s consists of lowercase English letters, '|' and '*'"
    )
    assert s.count("|") % 2 == 0, "s contains an even number of vertical bars '|'"
