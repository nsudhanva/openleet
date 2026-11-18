"""Cinema Seat Allocation: n rows and a list of reserved [row, seat] pairs."""


def check(n: int, reservedSeats: list[list[int]]) -> None:
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert 1 <= len(reservedSeats) <= min(10 * n, 10**4), (
        "1 <= reservedSeats.length <= min(10 * n, 10^4)"
    )
    assert all(len(s) == 2 for s in reservedSeats), "reservedSeats[i] == [rowi, seati]"
    assert all(1 <= r <= n for r, _ in reservedSeats), "1 <= rowi <= n"
    assert all(1 <= s <= 10 for _, s in reservedSeats), "1 <= seati <= 10"
    assert len({(r, s) for r, s in reservedSeats}) == len(reservedSeats), (
        "all reservedSeats[i] are distinct"
    )
