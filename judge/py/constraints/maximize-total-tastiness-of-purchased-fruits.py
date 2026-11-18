"""Maximize Total Tastiness of Purchased Fruits: prices, tastiness, budget, coupons."""


def check(price: list[int], tastiness: list[int], maxAmount: int, maxCoupons: int) -> None:
    n = len(price)
    assert len(tastiness) == n, "n == price.length == tastiness.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(0 <= v <= 1000 for v in price), "0 <= price[i] <= 1000"
    assert all(0 <= v <= 1000 for v in tastiness), "0 <= tastiness[i] <= 1000"
    assert 0 <= maxAmount <= 1000, "0 <= maxAmount <= 1000"
    assert 0 <= maxCoupons <= 5, "0 <= maxCoupons <= 5"
