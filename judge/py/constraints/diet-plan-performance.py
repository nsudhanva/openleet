"""Diet Plan Performance: daily calories, a window size and thresholds."""


def check(calories: list[int], k: int, lower: int, upper: int) -> None:
    assert 1 <= k <= len(calories) <= 10**5, "1 <= k <= calories.length <= 10^5"
    assert all(0 <= c <= 20000 for c in calories), "0 <= calories[i] <= 20000"
    assert 0 <= lower <= upper, "0 <= lower <= upper"
