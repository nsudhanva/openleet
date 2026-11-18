"""Find Longest Special Substring That Occurs Thrice II: a lowercase string."""


def check(s: str) -> None:
    assert 3 <= len(s) <= 5 * 10**5, "3 <= s.length <= 5 * 10^5"
    assert all(len(c) == 1 and "a" <= c <= "z" for c in s), (
        "s consists of only lowercase English letters"
    )
