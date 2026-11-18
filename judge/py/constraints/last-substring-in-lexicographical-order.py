"""Last Substring in Lexicographical Order: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 4 * 10**5, "1 <= s.length <= 4 * 10^5"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
