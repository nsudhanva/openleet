"""Design File System: FileSystem calls."""


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
    _shape(ops, args, "FileSystem", 0, {"createPath": 2, "get": 1})
    import re

    assert len(ops) - 1 <= 10**4, "at most 10^4 calls"
    for op, a in zip(ops[1:], args[1:], strict=True):
        p = a[0]
        assert isinstance(p, str) and 2 <= len(p) <= 100, "2 <= path.length <= 100"
        assert re.fullmatch(r"(/[a-z]+)+", p), "path is valid: '/' followed by lowercase names"
        if op == "createPath":
            assert isinstance(a[1], int) and 1 <= a[1] <= 10**9, "1 <= value <= 10^9"
