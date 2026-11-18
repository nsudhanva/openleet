"""Time Based Key-Value Store: TimeMap calls set(key, value, timestamp) and get(key, timestamp)."""


def _word(w: object, name: str) -> None:
    assert isinstance(w, str) and 1 <= len(w) <= 100, f"1 <= {name}.length <= 100"
    assert all(c in "abcdefghijklmnopqrstuvwxyz0123456789" for c in w), (
        f"{name} consists of lowercase English letters and digits"
    )


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have equal length"
    assert ops[0] == "TimeMap" and args[0] == [], "TimeMap() takes no arguments"
    assert len(ops) - 1 <= 2 * 10**5, "at most 2 * 10^5 calls to set and get"
    last = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "set":
            assert len(a) == 3, "set(key, value, timestamp)"
            _word(a[0], "key")
            _word(a[1], "value")
            assert isinstance(a[2], int) and 1 <= a[2] <= 10**7, "1 <= timestamp <= 10^7"
            assert a[2] > last, "timestamps of set are strictly increasing"
            last = a[2]
        else:
            assert op == "get" and len(a) == 2, "get(key, timestamp)"
            _word(a[0], "key")
            assert isinstance(a[1], int) and 1 <= a[1] <= 10**7, "1 <= timestamp <= 10^7"
