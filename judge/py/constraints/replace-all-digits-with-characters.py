"""Replace All Digits with Characters: lowercase letters at even indices, digits at odd indices."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c.isascii() and (c.islower() or c.isdigit()) for c in s), (
        "s consists only of lowercase English letters and digits"
    )
    for i in range(1, len(s), 2):
        assert s[i].isdigit() and s[i - 1].isalpha(), "digits sit at odd indices after a letter"
        assert ord(s[i - 1]) + int(s[i]) <= ord("z"), (
            "shift(s[i-1], s[i]) <= 'z' for all odd indices i"
        )
