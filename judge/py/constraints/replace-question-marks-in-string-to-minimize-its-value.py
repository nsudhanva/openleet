"""Replace Question Marks in String to Minimize Its Value: lowercase letters and '?'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c == "?" or "a" <= c <= "z" for c in s), "s[i] is a lowercase letter or '?'"
