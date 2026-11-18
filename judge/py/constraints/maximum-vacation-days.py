"""Maximum Vacation Days: an n x n flight matrix and an n x k vacation-days matrix."""


def check(flights: list[list[int]], days: list[list[int]]) -> None:
    n = len(flights)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in flights), "n == flights[i].length"
    assert len(days) == n, "n == days.length"
    k = len(days[0])
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert all(len(r) == k for r in days), "k == days[i].length"
    assert all(v in (0, 1) for r in flights for v in r), "flights[i][j] is either 0 or 1"
    assert all(flights[i][i] == 0 for i in range(n)), "flights[i][i] == 0"
    assert all(0 <= v <= 7 for r in days for v in r), "0 <= days[i][j] <= 7"
