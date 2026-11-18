"""Final Prices With a Special Discount in a Shop: a list of prices."""


def check(prices: list[int]) -> None:
    assert 1 <= len(prices) <= 500, "1 <= prices.length <= 500"
    assert all(1 <= p <= 1000 for p in prices), "1 <= prices[i] <= 1000"
