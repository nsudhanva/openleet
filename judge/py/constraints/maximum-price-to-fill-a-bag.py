"""Maximum Price to Fill a Bag: [price, weight] items and a bag capacity."""


def check(items: list[list[int]], capacity: int) -> None:
    assert 1 <= len(items) <= 10**5, "1 <= items.length <= 10^5"
    assert all(len(it) == 2 for it in items), "items[i].length == 2"
    assert all(1 <= p <= 10**4 and 1 <= w <= 10**4 for p, w in items), "1 <= price, weight <= 10^4"
    assert 1 <= capacity <= 10**9, "1 <= capacity <= 10^9"
