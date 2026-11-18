"""Find Longest Self-Contained Substring: a lowercase string."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 5 * 10**4, "2 <= s.length <= 5 * 10^4"
    assert all(len(c) == 1 and "a" <= c <= "z" for c in s), (
        "s consists only of lowercase English letters"
    )
