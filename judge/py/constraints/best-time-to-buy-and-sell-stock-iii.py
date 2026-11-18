"""Best Time to Buy and Sell Stock III: a list of daily prices."""


def check(prices: list[int]) -> None:
    assert 1 <= len(prices) <= 10**5, "1 <= prices.length <= 10^5"
    assert all(0 <= p <= 10**5 for p in prices), "0 <= prices[i] <= 10^5"
