"""Range Module: addRange / queryRange / removeRange calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "RangeModule" and len(args[0]) == 0, "constructor takes no arguments"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls"
    for op, a in zip(ops[1:], args[1:], strict=False):
        assert op in ("addRange", "queryRange", "removeRange") and len(a) == 2, (
            "calls take (left, right)"
        )
        assert 1 <= a[0] < a[1] <= 10**9, "1 <= left < right <= 10^9"
