"""Find the Occurrence of First Almost Equal Substring: a string s and a shorter pattern."""


def check(s: str, pattern: str) -> None:
    assert 1 <= len(pattern) < len(s) <= 10**5, "1 <= pattern.length < s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
    assert all("a" <= c <= "z" for c in pattern), (
        "pattern consists only of lowercase English letters"
    )
