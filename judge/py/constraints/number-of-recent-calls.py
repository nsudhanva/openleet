"""Number of Recent Calls: RecentCounter() followed by ping(t) calls."""

from itertools import pairwise


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have the same length"
    assert ops[0] == "RecentCounter" and args[0] == [], "RecentCounter() takes no arguments"
    pings = ops[1:]
    assert all(o == "ping" for o in pings), "only ping is called"
    assert len(pings) <= 10**4, "at most 10^4 calls will be made to ping"
    assert all(len(a) == 1 for a in args[1:]), "ping takes one argument"
    ts = [a[0] for a in args[1:]]
    assert all(1 <= t <= 10**9 for t in ts), "1 <= t <= 10^9"
    assert all(a < b for a, b in pairwise(ts)), "ping is called with strictly increasing t"
