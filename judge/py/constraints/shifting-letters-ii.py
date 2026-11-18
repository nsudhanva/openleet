"""Shifting Letters II: a lowercase string and [start, end, direction] shift ranges."""


def check(s: str, shifts: list[list[int]]) -> None:
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert 1 <= len(shifts) <= 5 * 10**4, "1 <= shifts.length <= 5 * 10^4"
    assert all("a" <= ch <= "z" for ch in s), "s consists of lowercase English letters"
    assert all(len(x) == 3 for x in shifts), "shifts[i].length == 3"
    assert all(0 <= a <= b < len(s) for a, b, _ in shifts), "0 <= starti <= endi < s.length"
    assert all(0 <= d <= 1 for _, _, d in shifts), "0 <= directioni <= 1"
