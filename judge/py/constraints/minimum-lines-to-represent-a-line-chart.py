"""Minimum Lines to Represent a Line Chart: [day, price] points with distinct days."""


def check(stockPrices: list[list[int]]) -> None:
    assert 1 <= len(stockPrices) <= 10**5, "1 <= stockPrices.length <= 10^5"
    assert all(len(p) == 2 for p in stockPrices), "stockPrices[i].length == 2"
    assert all(1 <= d <= 10**9 and 1 <= p <= 10**9 for d, p in stockPrices), (
        "1 <= day_i, price_i <= 10^9"
    )
    assert len({d for d, _ in stockPrices}) == len(stockPrices), "All day_i are distinct"
