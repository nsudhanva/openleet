"""Number of Orders in the Backlog: a list of [price, amount, orderType] batches."""


def check(orders: list[list[int]]) -> None:
    assert 1 <= len(orders) <= 10**5, "1 <= orders.length <= 10^5"
    assert all(len(o) == 3 for o in orders), "orders[i].length == 3"
    assert all(1 <= p <= 10**9 and 1 <= a <= 10**9 for p, a, _ in orders), (
        "1 <= pricei, amounti <= 10^9"
    )
    assert all(t in (0, 1) for _, _, t in orders), "orderTypei is either 0 or 1"
