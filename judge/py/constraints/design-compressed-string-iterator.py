"""Design Compressed String Iterator: StringIterator calls."""


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
    _shape(ops, args, "StringIterator", 1, {"next": 0, "hasNext": 0})
    import re

    s = args[0][0]
    assert isinstance(s, str) and 1 <= len(s) <= 1000, "1 <= compressedString.length <= 1000"
    assert re.fullmatch(r"([A-Za-z][0-9]+)+", s), (
        "letters each followed by a repetition count of digits"
    )
    for m in re.finditer(r"[A-Za-z]([0-9]+)", s):
        assert 1 <= int(m.group(1)) <= 10**9, "repetitions of a single character in [1, 10^9]"
    assert len(ops) - 1 <= 100, "at most 100 calls"
