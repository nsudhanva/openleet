"""Maximum Number of Items From Sale I: [factor, price] items and a budget."""


def check(items: list[list[int]], budget: int) -> None:
    assert 1 <= len(items) <= 1000, "1 <= items.length <= 1000"
    assert all(len(it) == 2 for it in items), "items[i] = [factori, pricei]"
    assert all(1 <= f <= 1500 and 1 <= p <= 1500 for f, p in items), "1 <= factori, pricei <= 1500"
    assert 1 <= budget <= 1500, "1 <= budget <= 1500"
