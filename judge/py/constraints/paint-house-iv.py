"""Paint House IV: an even number n of houses, each with the cost of painting it one of 3 colors."""


def check(n: int, cost: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert n % 2 == 0, "n is even"
    assert len(cost) == n, "cost.length == n"
    assert all(len(row) == 3 for row in cost), "cost[i].length == 3"
    assert all(0 <= c <= 10**5 for row in cost for c in row), "0 <= cost[i][j] <= 10^5"
