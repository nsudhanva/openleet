"""Map Sum Pairs: MapSum() followed by insert(key, val) and sum(prefix) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "one argument list per operation"
    assert ops[0] == "MapSum" and args[0] == [], "MapSum() takes no arguments"
    assert len(ops) - 1 <= 50, "at most 50 calls to insert and sum"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("insert", "sum"), "only insert and sum are called"
        assert len(a) == (2 if op == "insert" else 1), "insert(key, val), sum(prefix)"
        assert isinstance(a[0], str), "key and prefix are strings"
        assert 1 <= len(a[0]) <= 50, "1 <= key.length, prefix.length <= 50"
        assert all("a" <= c <= "z" for c in a[0]), "lowercase English letters only"
        if op == "insert":
            assert isinstance(a[1], int) and 1 <= a[1] <= 1000, "1 <= val <= 1000"
