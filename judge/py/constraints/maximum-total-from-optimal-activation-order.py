"""Maximum Total from Optimal Activation Order: parallel value and limit arrays."""


def check(value: list[int], limit: list[int]) -> None:
    n = len(value)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(limit) == n, "n == value.length == limit.length"
    assert all(1 <= v <= 10**5 for v in value), "1 <= value[i] <= 10^5"
    assert all(1 <= x <= n for x in limit), "1 <= limit[i] <= n"
