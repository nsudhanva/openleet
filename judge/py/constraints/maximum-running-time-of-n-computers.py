"""Maximum Running Time of N Computers: a computer count and battery capacities."""


def check(n: int, batteries: list[int]) -> None:
    assert 1 <= n <= len(batteries) <= 10**5, "1 <= n <= batteries.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in batteries), "1 <= batteries[i] <= 10^9"
