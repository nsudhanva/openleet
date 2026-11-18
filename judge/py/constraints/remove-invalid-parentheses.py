"""Remove Invalid Parentheses: a short string of lowercase letters and parentheses."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 25, "1 <= s.length <= 25"
    assert all(c in "()" or "a" <= c <= "z" for c in s), (
        "s consists of lowercase English letters and parentheses"
    )
    assert sum(c in "()" for c in s) <= 20, "at most 20 parentheses in s"
