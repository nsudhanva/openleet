"""Shifting Letters: a lowercase string and one shift amount per letter."""


def check(s: str, shifts: list[int]) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= ch <= "z" for ch in s), "s consists of lowercase English letters"
    assert len(shifts) == len(s), "shifts.length == s.length"
    assert all(0 <= x <= 10**9 for x in shifts), "0 <= shifts[i] <= 10^9"
