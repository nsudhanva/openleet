"""Find the Substring With Maximum Cost: a string s, distinct chars and their values."""


def check(s: str, chars: str, vals: list[int]) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert 1 <= len(chars) <= 26, "1 <= chars.length <= 26"
    assert all("a" <= c <= "z" for c in chars), "chars consist of lowercase English letters"
    assert len(set(chars)) == len(chars), "chars consist of distinct letters"
    assert len(vals) == len(chars), "vals.length == chars.length"
    assert all(-1000 <= v <= 1000 for v in vals), "-1000 <= vals[i] <= 1000"
