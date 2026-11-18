"""Make Costs of Paths Equal in a Binary Tree: a perfect binary tree with node costs."""


def check(n: int, cost: list[int]) -> None:
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert (n + 1) & n == 0, "n + 1 is a power of 2"
    assert len(cost) == n, "cost.length == n"
    assert all(1 <= c <= 10**4 for c in cost), "1 <= cost[i] <= 10^4"
