"""Seat Reservation Manager: SeatManager(n) with reserve() and unreserve(seatNumber) calls."""

import heapq


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "SeatManager" and len(args[0]) == 1, "SeatManager(n) comes first"
    assert all(o in ("reserve", "unreserve") for o in ops[1:]), "only reserve/unreserve follow"
    n = args[0][0]
    assert isinstance(n, int) and 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls to reserve and unreserve"
    free = list(range(1, n + 1))
    taken: set[int] = set()
    for o, a in zip(ops[1:], args[1:], strict=True):
        if o == "reserve":
            assert a == [], "reserve takes no arguments"
            assert free, "reserve is called only when an unreserved seat exists"
            taken.add(heapq.heappop(free))
        else:
            assert len(a) == 1 and isinstance(a[0], int), "unreserve takes seatNumber"
            assert 1 <= a[0] <= n, "1 <= seatNumber <= n"
            assert a[0] in taken, "unreserve is called only on a reserved seat"
            taken.remove(a[0])
            heapq.heappush(free, a[0])
