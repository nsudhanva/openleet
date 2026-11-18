"""Paint House III: m houses (0 = unpainted), n colors, a cost grid and a neighborhood target."""


def check(houses: list[int], cost: list[list[int]], m: int, n: int, target: int) -> None:
    assert isinstance(houses, list) and isinstance(cost, list), "houses and cost are lists"
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert len(houses) == m == len(cost), "m == houses.length == cost.length"
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(row) == n for row in cost), "n == cost[i].length"
    assert 1 <= target <= m, "1 <= target <= m"
    assert all(0 <= h <= n for h in houses), "0 <= houses[i] <= n"
    assert all(1 <= c <= 10**4 for row in cost for c in row), "1 <= cost[i][j] <= 10^4"
