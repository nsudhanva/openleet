"""Total Appeal of A String: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
