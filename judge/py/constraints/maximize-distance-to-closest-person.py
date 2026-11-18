"""Maximize Distance to Closest Person: a row of seats, 1 occupied and 0 empty."""


def check(seats: list[int]) -> None:
    assert 2 <= len(seats) <= 2 * 10**4, "2 <= seats.length <= 2 * 10^4"
    assert all(v in (0, 1) for v in seats), "seats[i] is 0 or 1"
    assert 0 in seats, "at least one seat is empty"
    assert 1 in seats, "at least one seat is occupied"
