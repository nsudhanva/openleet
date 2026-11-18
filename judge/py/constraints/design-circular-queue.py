"""Design Circular Queue: MyCircularQueue calls."""


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
    _shape(
        ops,
        args,
        "MyCircularQueue",
        1,
        {"enQueue": 1, "deQueue": 0, "Front": 0, "Rear": 0, "isEmpty": 0, "isFull": 0},
    )
    assert isinstance(args[0][0], int) and 1 <= args[0][0] <= 1000, "1 <= k <= 1000"
    assert len(ops) - 1 <= 3000, "at most 3000 calls"
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "enQueue":
            assert isinstance(a[0], int) and 0 <= a[0] <= 1000, "0 <= value <= 1000"
