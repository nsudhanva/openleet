"""Design an ATM Machine: ATM calls."""


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
    _shape(ops, args, "ATM", 0, {"deposit": 1, "withdraw": 1})
    assert len(ops) - 1 <= 5000, "at most 5000 calls"
    assert "deposit" in ops and "withdraw" in ops, (
        "at least one call to each of withdraw and deposit"
    )
    totals = [0] * 5
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "deposit":
            b = a[0]
            assert isinstance(b, list) and len(b) == 5, "banknotesCount.length == 5"
            assert all(isinstance(x, int) and 0 <= x <= 10**9 for x in b), (
                "0 <= banknotesCount[i] <= 10^9"
            )
            for i in range(5):
                totals[i] += b[i]
            assert all(t <= 10**9 for t in totals), (
                "sum of banknotesCount[i] in all deposits <= 10^9"
            )
        else:
            assert isinstance(a[0], int) and 1 <= a[0] <= 10**9, "1 <= amount <= 10^9"
