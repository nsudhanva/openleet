"""Paint House: n houses, each with the cost of painting it one of 3 colors."""


def check(costs: list[list[int]]) -> None:
    assert 1 <= len(costs) <= 100, "1 <= n <= 100"
    assert all(len(row) == 3 for row in costs), "costs[i].length == 3"
    assert all(1 <= c <= 20 for row in costs for c in row), "1 <= costs[i][j] <= 20"
