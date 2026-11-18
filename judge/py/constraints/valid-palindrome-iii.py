"""Valid Palindrome III: a lowercase string and a removal budget k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
