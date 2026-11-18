"""String Transformation: two equal-length lowercase strings and a step count k."""


def check(s: str, t: str, k: int) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 2 <= len(s) <= 5 * 10**5, "2 <= s.length <= 5 * 10^5"
    assert len(s) == len(t), "s.length == t.length"
    assert isinstance(k, int) and 1 <= k <= 10**15, "1 <= k <= 10^15"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert all("a" <= c <= "z" for c in t), "t consists of only lowercase English letters"
