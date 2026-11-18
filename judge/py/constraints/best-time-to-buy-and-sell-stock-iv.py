"""Best Time to Buy and Sell Stock IV: a transaction limit k and daily prices."""


def check(k: int, prices: list[int]) -> None:
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert 1 <= len(prices) <= 1000, "1 <= prices.length <= 1000"
    assert all(0 <= p <= 1000 for p in prices), "0 <= prices[i] <= 1000"
