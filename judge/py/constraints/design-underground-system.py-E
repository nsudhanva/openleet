"""Design Underground System: checkIn/checkOut/getAverageTime calls."""

import re


def _name(s) -> bool:
    return isinstance(s, str) and re.fullmatch(r"[A-Za-z0-9]{1,10}", s) is not None


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert args[0] == [], "UndergroundSystem()"
    assert len(ops) - 1 <= 2 * 10**4, "at most 2 * 10^4 calls"
    inside: dict[int, int] = {}
    trips: set[tuple[str, str]] = set()
    starts: dict[int, str] = {}
    last_t = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op in ("checkIn", "checkOut"):
            assert len(a) == 3 and isinstance(a[0], int) and isinstance(a[2], int), (
                f"{op}(id, stationName, t)"
            )
            cid, station, t = a
            assert 1 <= cid <= 10**6 and 1 <= t <= 10**6, "1 <= id, t <= 10^6"
            assert _name(station), "stationName: 1..10 letters and digits"
            assert t >= last_t, "all events happen in chronological order"
            last_t = t
            if op == "checkIn":
                assert cid not in inside, "a customer can only be checked into one place at a time"
                inside[cid] = t
                starts[cid] = station
            else:
                assert cid in inside, "checkOut follows a checkIn"
                assert inside.pop(cid) < t, "t1 < t2"
                trips.add((starts.pop(cid), station))
        elif op == "getAverageTime":
            assert len(a) == 2 and _name(a[0]) and _name(a[1]), "stations: 1..10 letters and digits"
            assert (a[0], a[1]) in trips, "at least one customer traveled between the stations"
        else:
            raise AssertionError("unknown operation")
