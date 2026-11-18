"""Best Sightseeing Pair: a list of sightseeing spot values."""


def check(values: list[int]) -> None:
    assert 2 <= len(values) <= 5 * 10**4, "2 <= values.length <= 5 * 10^4"
    assert all(1 <= v <= 1000 for v in values), "1 <= values[i] <= 1000"
