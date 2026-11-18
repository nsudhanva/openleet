"""The Latest Time to Catch a Bus: bus departure times, passenger arrival times and a capacity."""


def check(buses: list[int], passengers: list[int], capacity: int) -> None:
    assert 1 <= len(buses) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(passengers) <= 10**5, "1 <= m <= 10^5"
    assert 1 <= capacity <= 10**5, "1 <= capacity <= 10^5"
    assert all(2 <= b <= 10**9 for b in buses), "2 <= buses[i] <= 10^9"
    assert all(2 <= p <= 10**9 for p in passengers), "2 <= passengers[i] <= 10^9"
    assert len(set(buses)) == len(buses), "each element in buses is unique"
    assert len(set(passengers)) == len(passengers), "each element in passengers is unique"
