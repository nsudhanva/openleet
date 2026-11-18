"""Design Hit Counter: HitCounter calls."""


def _shape(ops, args, ctor, ctor_arity, sig):
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == ctor, "first operation is the constructor"
    assert all(isinstance(a, list) for a in args), "each args[i] is a list"
    assert len(args[0]) == ctor_arity, "constructor argument count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in sig, "known method name"
        assert len(a) == sig[op], "argument count of " + op


def check(ops: list[str], args: list[list]) -> None:
    _shape(ops, args, "HitCounter", 0, {"hit": 1, "getHits": 1})
    assert len(ops) - 1 <= 300, "at most 300 calls"
    last = 0
    for a in args[1:]:
        t = a[0]
        assert isinstance(t, int) and 1 <= t <= 2 * 10**9, "1 <= timestamp <= 2 * 10^9"
        assert t >= last, "calls are in chronological order"
        last = t
