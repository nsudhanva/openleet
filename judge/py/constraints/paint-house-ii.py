"""Paint House II: n houses, each with the cost of painting it one of k colors."""


def check(costs: list[list[int]]) -> None:
    n = len(costs)
    assert 1 <= n <= 100, "1 <= n <= 100"
    k = len(costs[0])
    assert 2 <= k <= 20, "2 <= k <= 20"
    assert all(len(row) == k for row in costs), "costs[i].length == k"
    assert all(1 <= c <= 20 for row in costs for c in row), "1 <= costs[i][j] <= 20"
