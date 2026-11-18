"""Beautiful Towers II: a list of maximum tower heights."""


def check(maxHeights: list[int]) -> None:
    assert 1 <= len(maxHeights) <= 10**5, "1 <= n == maxHeights.length <= 10^5"
    assert all(1 <= h <= 10**9 for h in maxHeights), "1 <= maxHeights[i] <= 10^9"
