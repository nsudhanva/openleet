"""Container With Most Water: a list of line heights."""


def check(height: list[int]) -> None:
    assert isinstance(height, list), "height is a list"
    assert 2 <= len(height) <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) for v in height), "height[i] is an integer"
    assert all(0 <= v <= 10**4 for v in height), "0 <= height[i] <= 10^4"
