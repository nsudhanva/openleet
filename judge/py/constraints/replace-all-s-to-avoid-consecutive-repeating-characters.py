"""Replace All ?s to Avoid Consecutive Repeating Characters: lowercase letters and ?."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c == "?" or "a" <= c <= "z" for c in s), "s consists of lowercase letters and '?'"
