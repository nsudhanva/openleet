"""First Letter to Appear Twice: a lowercase string with a repeated letter."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 100, "2 <= s.length <= 100"
    assert all(c.isascii() and c.islower() for c in s), "s consists of lowercase English letters"
    assert len(set(s)) < len(s), "s has at least one repeated letter"
