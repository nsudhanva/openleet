"""Find Longest Special Substring That Occurs Thrice I: a short lowercase string."""


def check(s: str) -> None:
    assert 3 <= len(s) <= 50, "3 <= s.length <= 50"
    assert all(len(c) == 1 and "a" <= c <= "z" for c in s), (
        "s consists of only lowercase English letters"
    )
