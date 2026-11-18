"""Describe the Painting: colored half-closed segments [start, end, color)."""


def check(segments: list[list[int]]) -> None:
    assert 1 <= len(segments) <= 2 * 10**4, "1 <= segments.length <= 2 * 10^4"
    assert all(len(s) == 3 for s in segments), "segments[i].length == 3"
    assert all(1 <= s[0] < s[1] <= 10**5 for s in segments), "1 <= starti < endi <= 10^5"
    assert all(1 <= s[2] <= 10**9 for s in segments), "1 <= colori <= 10^9"
    colors = [s[2] for s in segments]
    assert len(set(colors)) == len(colors), "each colori is distinct"
