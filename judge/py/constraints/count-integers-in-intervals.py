"""Count Integers in Intervals: design class with add(left, right) and count()."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have equal length"
    assert ops[0] == "CountIntervals" and args[0] == [], "the constructor takes no arguments"
    calls = ops[1:]
    assert all(o in ("add", "count") for o in calls), "only add and count are called"
    assert len(calls) <= 10**5, "at most 10^5 calls to add and count"
    assert "count" in calls, "at least one call to count"
    for o, a in zip(calls, args[1:], strict=True):
        if o == "add":
            assert len(a) == 2, "add takes left and right"
            assert 1 <= a[0] <= a[1] <= 10**9, "1 <= left <= right <= 10^9"
        else:
            assert a == [], "count takes no arguments"
