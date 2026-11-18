"""Design an Ordered Stream: OrderedStream calls."""


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
    _shape(ops, args, "OrderedStream", 1, {"insert": 2})
    n = args[0][0]
    assert isinstance(n, int) and 1 <= n <= 1000, "1 <= n <= 1000"
    assert len(ops) - 1 == n, "exactly n calls to insert"
    seen = set()
    for _, (i, v) in zip(ops[1:], args[1:], strict=True):
        assert isinstance(i, int) and 1 <= i <= n, "1 <= id <= n"
        assert i not in seen, "each call to insert has a unique id"
        seen.add(i)
        assert isinstance(v, str) and len(v) == 5, "value.length == 5"
        assert all("a" <= c <= "z" for c in v), "value consists only of lowercase letters"
