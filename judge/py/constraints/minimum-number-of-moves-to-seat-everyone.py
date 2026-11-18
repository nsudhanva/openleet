"""Minimum Number of Moves to Seat Everyone: seat positions and student positions."""


def check(seats: list[int], students: list[int]) -> None:
    assert isinstance(seats, list) and isinstance(students, list), "arrays"
    n = len(seats)
    assert n == len(students), "n == seats.length == students.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in seats), "1 <= seats[i] <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in students), "1 <= students[j] <= 100"
