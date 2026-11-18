"""Best Time to Buy and Sell Stock using Strategy: prices, a strategy and an even k."""


def check(prices: list[int], strategy: list[int], k: int) -> None:
    assert isinstance(k, int), "k is an integer"
    assert 2 <= len(prices) <= 10**5, "2 <= prices.length <= 10^5"
    assert len(prices) == len(strategy), "prices.length == strategy.length"
    assert all(1 <= p <= 10**5 for p in prices), "1 <= prices[i] <= 10^5"
    assert all(s in (-1, 0, 1) for s in strategy), "-1 <= strategy[i] <= 1"
    assert 2 <= k <= len(prices), "2 <= k <= prices.length"
    assert k % 2 == 0, "k is even"
