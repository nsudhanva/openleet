"""Capacity To Ship Packages Within D Days: package weights and a number of days."""


def check(weights: list[int], days: int) -> None:
    assert isinstance(weights, list) and isinstance(days, int), "weights is a list, days an int"
    assert 1 <= days <= len(weights) <= 5 * 10**4, "1 <= days <= weights.length <= 5 * 10^4"
    assert all(isinstance(w, int) and 1 <= w <= 500 for w in weights), "1 <= weights[i] <= 500"
