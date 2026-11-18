"""Count Pairs That Form a Complete Day II: an array of hours."""


def check(hours: list[int]) -> None:
    assert 1 <= len(hours) <= 5 * 10**5, "1 <= hours.length <= 5 * 10^5"
    assert all(1 <= h <= 10**9 for h in hours), "1 <= hours[i] <= 10^9"
