"""Moving Average from Data Stream: a MovingAverage(size) constructor then next(val) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "MovingAverage" and len(args[0]) == 1, "constructor is MovingAverage(size)"
    assert 1 <= args[0][0] <= 1000, "1 <= size <= 1000"
    assert all(op == "next" for op in ops[1:]), "only next is called after construction"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls will be made to next"
    for a in args[1:]:
        assert len(a) == 1, "next takes one argument"
        assert -(10**5) <= a[0] <= 10**5, "-10^5 <= val <= 10^5"
