"""Corporate Flight Bookings: [first, last, seats] bookings over n flights."""


def check(bookings: list[list[int]], n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert isinstance(bookings, list), "bookings is a list"
    assert 1 <= len(bookings) <= 2 * 10**4, "1 <= bookings.length <= 2 * 10^4"
    assert all(isinstance(b, list) and len(b) == 3 for b in bookings), "bookings[i].length == 3"
    assert all(isinstance(v, int) for b in bookings for v in b), "bookings[i] holds integers"
    assert all(1 <= f <= la <= n for f, la, _ in bookings), "1 <= firsti <= lasti <= n"
    assert all(1 <= s <= 10**4 for _, _, s in bookings), "1 <= seatsi <= 10^4"
