"""Reverse Substrings Between Each Pair of Parentheses: a string of lowercase letters and balanced
parentheses."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2000, "1 <= s.length <= 2000"
    assert all("a" <= c <= "z" or c in "()" for c in s), (
        "s only contains lowercase letters and parentheses"
    )
    depth = 0
    for c in s:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            assert depth >= 0, "all parentheses are balanced"
    assert depth == 0, "all parentheses are balanced"
