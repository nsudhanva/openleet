"""Daily Temperatures: a list of daily temperatures."""


def check(temperatures: list[int]) -> None:
    assert 1 <= len(temperatures) <= 10**5, "1 <= temperatures.length <= 10^5"
    assert all(30 <= t <= 100 for t in temperatures), "30 <= temperatures[i] <= 100"
