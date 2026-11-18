"""Maximize Area of Square Hole in Grid: grid size and removable bar positions."""


def check(n: int, m: int, hBars: list[int], vBars: list[int]) -> None:
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert 1 <= m <= 10**9, "1 <= m <= 10^9"
    assert 1 <= len(hBars) <= 100, "1 <= hBars.length <= 100"
    assert all(2 <= b <= n + 1 for b in hBars), "2 <= hBars[i] <= n + 1"
    assert 1 <= len(vBars) <= 100, "1 <= vBars.length <= 100"
    assert all(2 <= b <= m + 1 for b in vBars), "2 <= vBars[i] <= m + 1"
    assert len(set(hBars)) == len(hBars), "all values in hBars are distinct"
    assert len(set(vBars)) == len(vBars), "all values in vBars are distinct"
