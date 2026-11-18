"""Maximum Tastiness of Candy Basket: candy prices and a basket size k."""


def check(price: list[int], k: int) -> None:
    assert 2 <= k <= len(price) <= 10**5, "2 <= k <= price.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in price), "1 <= price[i] <= 10^9"
