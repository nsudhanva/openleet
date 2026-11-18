"""Trapping Rain Water: elevation heights."""


def check(height: list[int]) -> None:
    assert 1 <= len(height) <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert all(0 <= h <= 10**5 for h in height), "0 <= height[i] <= 10^5"
