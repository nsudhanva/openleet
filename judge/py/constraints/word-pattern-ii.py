"""Word Pattern II: a lowercase pattern and a lowercase string."""


def check(pattern: str, s: str) -> None:
    assert 1 <= len(pattern) <= 20, "1 <= pattern.length <= 20"
    assert 1 <= len(s) <= 20, "1 <= s.length <= 20"
    assert all("a" <= c <= "z" for c in pattern), (
        "pattern consists of only lowercase English letters"
    )
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
