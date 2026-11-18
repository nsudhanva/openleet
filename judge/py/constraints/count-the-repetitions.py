"""Count The Repetitions: strings s1, s2 and repeat counts n1, n2."""


def check(s1: str, n1: int, s2: str, n2: int) -> None:
    assert isinstance(s1, str) and isinstance(s2, str), "s1 and s2 are strings"
    assert 1 <= len(s1) <= 100, "1 <= s1.length <= 100"
    assert 1 <= len(s2) <= 100, "1 <= s2.length <= 100"
    assert all("a" <= c <= "z" for c in s1 + s2), "s1 and s2 consist of lowercase English letters"
    assert 1 <= n1 <= 10**6, "1 <= n1 <= 10^6"
    assert 1 <= n2 <= 10**6, "1 <= n2 <= 10^6"
