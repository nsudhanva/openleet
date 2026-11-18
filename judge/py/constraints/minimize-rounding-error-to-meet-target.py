"""Minimize Rounding Error to Meet Target: price strings with 3 decimals and an integer target."""

import re


def check(prices: list[str], target: int) -> None:
    assert 1 <= len(prices) <= 500, "1 <= prices.length <= 500"
    assert all(re.fullmatch(r"\d+\.\d{3}", p) for p in prices), (
        "each price is a real number with exactly 3 decimal places"
    )
    assert all(0 <= int(p.replace(".", "")) <= 1_000_000 for p in prices), (
        "each price is in [0.0, 1000.0]"
    )
    assert 0 <= target <= 10**6, "0 <= target <= 10^6"
