"""LRU Cache: LRUCache(capacity) followed by get(key) and put(key, value) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "one argument list per operation"
    assert ops[0] == "LRUCache", "first operation is the constructor"
    assert len(args[0]) == 1 and isinstance(args[0][0], int), "LRUCache(capacity)"
    assert 1 <= args[0][0] <= 3000, "1 <= capacity <= 3000"
    assert len(ops) - 1 <= 2 * 10**5, "at most 2 * 10^5 calls"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("get", "put"), "only get and put are called"
        assert len(a) == (1 if op == "get" else 2), "get(key), put(key, value)"
        assert all(isinstance(x, int) for x in a), "arguments are integers"
        assert 0 <= a[0] <= 10**4, "0 <= key <= 10^4"
        if op == "put":
            assert 0 <= a[1] <= 10**5, "0 <= value <= 10^5"
