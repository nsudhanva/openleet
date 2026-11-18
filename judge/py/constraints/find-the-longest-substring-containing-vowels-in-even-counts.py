"""Find the Longest Substring Containing Vowels in Even Counts: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 5 * 10**5, "1 <= s.length <= 5 x 10^5"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
