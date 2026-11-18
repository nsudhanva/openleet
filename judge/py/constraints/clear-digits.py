"""Clear Digits: a string of lowercase letters and digits."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c.isascii() and (c.islower() or c.isdigit()) for c in s), (
        "s consists only of lowercase English letters and digits"
    )
    letters = 0
    for c in s:
        if c.isdigit():
            assert letters > 0, "it is possible to delete all digits"
            letters -= 1
        else:
            letters += 1
