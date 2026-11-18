"""Longest Palindrome After Substring Concatenation I: two lowercase strings."""


def check(s: str, t: str) -> None:
    for name, v in (("s", s), ("t", t)):
        assert isinstance(v, str), f"{name} is a string"
        assert 1 <= len(v) <= 30, f"1 <= {name}.length <= 30"
        assert all("a" <= c <= "z" for c in v), f"{name} consists of lowercase English letters"
