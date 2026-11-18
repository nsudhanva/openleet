"""Buy Two Chocolates: chocolate prices and money."""


def check(prices: list[int], money: int) -> None:
    assert 2 <= len(prices) <= 50, "2 <= prices.length <= 50"
    assert all(1 <= p <= 100 for p in prices), "1 <= prices[i] <= 100"
    assert 1 <= money <= 100, "1 <= money <= 100"
