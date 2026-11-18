"""Total Characters in String After Transformations I: a lowercase string and t transformations."""


def check(s: str, t: int) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
    assert 1 <= t <= 10**5, "1 <= t <= 10^5"
