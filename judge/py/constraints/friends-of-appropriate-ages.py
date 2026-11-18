"""Friends Of Appropriate Ages: an array of ages."""


def check(ages: list[int]) -> None:
    assert 1 <= len(ages) <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert all(1 <= a <= 120 for a in ages), "1 <= ages[i] <= 120"
