"""LFU Cache: a constructor call followed by get and put calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "one argument list per operation"
    assert ops[0] == "LFUCache", "the first operation is the constructor"
    assert len(args[0]) == 1, "LFUCache(capacity)"
    assert 1 <= args[0][0] <= 10**4, "1 <= capacity <= 10^4"
    assert len(ops) - 1 <= 2 * 10**5, "at most 2 * 10^5 calls to get and put"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("get", "put"), "only get and put are called"
        if op == "get":
            assert len(a) == 1, "get(key)"
        else:
            assert len(a) == 2, "put(key, value)"
            assert 0 <= a[1] <= 10**9, "0 <= value <= 10^9"
        assert 0 <= a[0] <= 10**5, "0 <= key <= 10^5"
