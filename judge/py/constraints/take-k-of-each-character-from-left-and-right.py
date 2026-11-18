"""Take K of Each Character From Left and Right: a string over a, b, c and k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert set(s) <= set("abc"), "s consists of only the letters 'a', 'b', and 'c'"
    assert 0 <= k <= len(s), "0 <= k <= s.length"
