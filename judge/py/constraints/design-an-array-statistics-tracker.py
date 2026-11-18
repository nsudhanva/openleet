"""Design an Array Statistics Tracker: StatisticsTracker calls."""


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
        "StatisticsTracker",
        0,
        {"addNumber": 1, "removeFirstAddedNumber": 0, "getMean": 0, "getMedian": 0, "getMode": 0},
    )
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls"
    size = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "addNumber":
            assert isinstance(a[0], int) and 1 <= a[0] <= 10**9, "1 <= number <= 10^9"
            size += 1
        else:
            assert size >= 1, "remove/getMean/getMedian/getMode only with at least one element"
            if op == "removeFirstAddedNumber":
                size -= 1
