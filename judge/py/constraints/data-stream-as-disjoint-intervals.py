"""Data Stream as Disjoint Intervals: SummaryRanges calls addNum and getIntervals."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "SummaryRanges" and args[0] == [], "the constructor takes no arguments"
    calls = ops[1:]
    assert all(o in ("addNum", "getIntervals") for o in calls), (
        "only addNum and getIntervals are called"
    )
    assert len(calls) <= 3 * 10**4, "at most 3 * 10^4 calls to addNum and getIntervals"
    assert calls.count("getIntervals") <= 10**2, "at most 10^2 calls to getIntervals"
    for o, a in zip(ops[1:], args[1:], strict=True):
        if o == "addNum":
            assert len(a) == 1 and 0 <= a[0] <= 10**4, "0 <= value <= 10^4"
        else:
            assert a == [], "getIntervals takes no arguments"
