"""Best Time to Buy and Sell Stock with Cooldown: a list of daily prices."""


def check(prices: list[int]) -> None:
    assert 1 <= len(prices) <= 5000, "1 <= prices.length <= 5000"
    assert all(0 <= p <= 1000 for p in prices), "0 <= prices[i] <= 1000"
