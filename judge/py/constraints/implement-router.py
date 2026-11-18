"""Implement Router: calls on a Router(memoryLimit)."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops and ops[0] == "Router", "constructor first"
    assert len(args[0]) == 1, "Router takes memoryLimit"
    assert 2 <= args[0][0] <= 10**5, "2 <= memoryLimit <= 10^5"
    assert len(ops) - 1 <= 10**5, (
        "At most 10^5 calls will be made to addPacket, forwardPacket, and getCount altogether"
    )
    last = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "addPacket":
            assert len(a) == 3, "addPacket takes source, destination, timestamp"
            s, d, t = a
            assert 1 <= s <= 2 * 10**5 and 1 <= d <= 2 * 10**5, (
                "1 <= source, destination <= 2 * 10^5"
            )
            assert 1 <= t <= 10**9, "1 <= timestamp <= 10^9"
            assert t >= last, "addPacket is called in non-decreasing order of timestamp"
            last = t
        elif op == "forwardPacket":
            assert a == [], "forwardPacket takes no arguments"
        else:
            assert op == "getCount", "only addPacket, forwardPacket, getCount are called"
            assert len(a) == 3, "getCount takes destination, startTime, endTime"
            d, lo, hi = a
            assert 1 <= d <= 2 * 10**5, "1 <= destination <= 2 * 10^5"
            assert 1 <= lo <= hi <= 10**9, "1 <= startTime <= endTime <= 10^9"
