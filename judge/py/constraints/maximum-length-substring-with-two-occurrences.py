"""Maximum Length Substring With Two Occurrences: a lowercase string."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 100, "2 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
