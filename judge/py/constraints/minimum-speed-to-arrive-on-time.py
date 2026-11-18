"""Minimum Speed to Arrive on Time: train ride distances and a real-valued hour limit."""

from decimal import Decimal
from typing import cast


def check(dist: list[int], hour: float) -> None:
    assert 1 <= len(dist) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= d <= 10**5 for d in dist), "1 <= dist[i] <= 10^5"
    assert 1 <= hour <= 10**9, "1 <= hour <= 10^9"
    assert cast(int, Decimal(str(hour)).as_tuple().exponent) >= -2, (
        "at most two digits after the decimal point in hour"
    )
