"""Maximum Number of Alloys: machine compositions, stock and metal costs under a budget."""


def check(
    n: int,
    k: int,
    budget: int,
    composition: list[list[int]],
    stock: list[int],
    cost: list[int],
) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert 0 <= budget <= 10**8, "0 <= budget <= 10^8"
    assert len(composition) == k, "composition.length == k"
    assert all(len(row) == n for row in composition), "composition[i].length == n"
    assert all(1 <= v <= 100 for row in composition for v in row), "1 <= composition[i][j] <= 100"
    assert len(stock) == n and len(cost) == n, "stock.length == cost.length == n"
    assert all(0 <= v <= 10**8 for v in stock), "0 <= stock[i] <= 10^8"
    assert all(1 <= v <= 100 for v in cost), "1 <= cost[i] <= 100"
