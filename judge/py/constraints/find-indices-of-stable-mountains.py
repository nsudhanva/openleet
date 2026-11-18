"""Find Indices of Stable Mountains: mountain heights and a threshold."""


def check(height: list[int], threshold: int) -> None:
    assert 2 <= len(height) <= 100, "2 <= n == height.length <= 100"
    assert all(1 <= h <= 100 for h in height), "1 <= height[i] <= 100"
    assert 1 <= threshold <= 100, "1 <= threshold <= 100"
