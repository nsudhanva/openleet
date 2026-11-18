"""String Compression II: a lowercase string and a deletion budget k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
    assert isinstance(k, int) and 0 <= k <= len(s), "0 <= k <= s.length"
