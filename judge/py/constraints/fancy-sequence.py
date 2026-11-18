"""Fancy Sequence: a Fancy() design with append, addAll, multAll and getIndex calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == "Fancy" and args[0] == [], "the constructor is Fancy()"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls in total"
    for op, a in zip(ops[1:], args[1:], strict=False):
        assert len(a) == 1, "each call takes one argument"
        v = a[0]
        assert isinstance(v, int), "arguments are integers"
        if op == "append":
            assert 1 <= v <= 100, "1 <= val <= 100"
        elif op == "addAll":
            assert 1 <= v <= 100, "1 <= inc <= 100"
        elif op == "multAll":
            assert 1 <= v <= 100, "1 <= m <= 100"
        else:
            assert op == "getIndex", "calls are append, addAll, multAll and getIndex"
            assert 0 <= v <= 10**5, "0 <= idx <= 10^5"
