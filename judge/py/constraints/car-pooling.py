"""Car Pooling: trips as [passengers, from, to] and a capacity."""


def check(trips: list[list[int]], capacity: int) -> None:
    assert isinstance(trips, list), "trips is a list"
    assert 1 <= len(trips) <= 1000, "1 <= trips.length <= 1000"
    assert all(isinstance(t, list) and len(t) == 3 for t in trips), "trips[i].length == 3"
    assert all(1 <= p <= 100 for p, _, _ in trips), "1 <= numPassengers[i] <= 100"
    assert all(0 <= a < b <= 1000 for _, a, b in trips), "0 <= from[i] < to[i] <= 1000"
    assert 1 <= capacity <= 10**5, "1 <= capacity <= 10^5"
