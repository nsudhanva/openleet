"""Number of Smooth Descent Periods of a Stock: daily prices."""


def check(prices: list[int]) -> None:
    assert 1 <= len(prices) <= 10**5, "1 <= prices.length <= 10^5"
    assert all(1 <= p <= 10**5 for p in prices), "1 <= prices[i] <= 10^5"
