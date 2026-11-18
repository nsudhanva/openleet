"""Best Time to Buy and Sell Stock II: a list of daily prices."""


def check(prices: list[int]) -> None:
    assert 1 <= len(prices) <= 3 * 10**4, "1 <= prices.length <= 3 * 10^4"
    assert all(0 <= p <= 10**4 for p in prices), "0 <= prices[i] <= 10^4"
