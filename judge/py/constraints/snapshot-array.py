"""Snapshot Array: calls to set, snap and get on an array of given length."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "SnapshotArray" and len(args[0]) == 1, "constructor takes length"
    length = args[0][0]
    assert 1 <= length <= 5 * 10**4, "1 <= length <= 5 * 10^4"
    calls = list(zip(ops[1:], args[1:], strict=True))
    assert len(calls) <= 5 * 10**4, "at most 5 * 10^4 calls to set, snap, and get"
    assert all(op in ("set", "snap", "get") for op, _ in calls), "only set, snap, get are called"
    snaps = sum(op == "snap" for op, _ in calls)
    for op, a in calls:
        if op == "set":
            assert len(a) == 2, "set takes index and val"
            assert 0 <= a[0] < length, "0 <= index < length"
            assert 0 <= a[1] <= 10**9, "0 <= val <= 10^9"
        elif op == "snap":
            assert a == [], "snap takes no arguments"
        else:
            assert len(a) == 2, "get takes index and snap_id"
            assert 0 <= a[0] < length, "0 <= index < length"
            assert 0 <= a[1] < snaps, "0 <= snap_id < the number of snap() calls"
