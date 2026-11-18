"""Design a Stack With Increment Operation: CustomStack calls."""


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
    _shape(ops, args, "CustomStack", 1, {"push": 1, "pop": 0, "increment": 2})
    assert 1 <= args[0][0] <= 1000, "1 <= maxSize <= 1000"
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "push":
            assert 1 <= a[0] <= 1000, "1 <= x <= 1000"
        elif op == "increment":
            assert 1 <= a[0] <= 1000, "1 <= k <= 1000"
            assert 0 <= a[1] <= 100, "0 <= val <= 100"
    for name in ("push", "pop", "increment"):
        assert ops[1:].count(name) <= 1000, "at most 1000 calls to each method"
