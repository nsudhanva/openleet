"""Number of Lines To Write String: 26 letter widths and a lowercase string."""


def check(widths: list[int], s: str) -> None:
    assert len(widths) == 26, "widths.length == 26"
    assert all(2 <= w <= 10 for w in widths), "2 <= widths[i] <= 10"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
