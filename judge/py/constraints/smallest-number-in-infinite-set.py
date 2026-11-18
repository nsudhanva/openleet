"""Smallest Number in Infinite Set: calls to addBack and popSmallest."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "SmallestInfiniteSet" and args[0] == [], "constructor takes no arguments"
    calls = ops[1:]
    assert len(calls) <= 1000, "at most 1000 calls to popSmallest and addBack"
    for op, a in zip(calls, args[1:], strict=True):
        assert op in ("addBack", "popSmallest"), "only addBack and popSmallest are called"
        if op == "addBack":
            assert len(a) == 1 and 1 <= a[0] <= 1000, "1 <= num <= 1000"
        else:
            assert a == [], "popSmallest takes no arguments"
