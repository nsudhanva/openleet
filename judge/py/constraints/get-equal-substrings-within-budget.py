"""Get Equal Substrings Within Budget: two lowercase strings of equal length and a budget."""


def check(s: str, t: str, maxCost: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert len(t) == len(s), "t.length == s.length"
    assert 0 <= maxCost <= 10**6, "0 <= maxCost <= 10^6"
    assert all("a" <= c <= "z" for c in s + t), "s and t consist of only lowercase English letters"
