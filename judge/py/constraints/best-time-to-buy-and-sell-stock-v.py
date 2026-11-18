"""Best Time to Buy and Sell Stock V: daily prices and a transaction limit k."""


def check(prices: list[int], k: int) -> None:
    assert isinstance(k, int), "k is an integer"
    assert 2 <= len(prices) <= 10**3, "2 <= prices.length <= 10^3"
    assert all(1 <= p <= 10**9 for p in prices), "1 <= prices[i] <= 10^9"
    assert 1 <= k <= len(prices) / 2, "1 <= k <= prices.length / 2"
