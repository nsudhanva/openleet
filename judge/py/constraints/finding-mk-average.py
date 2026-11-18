"""Finding MK Average: calls on an MKAverage stream, constructed with m and k."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per call"
    assert ops[0] == "MKAverage" and len(args[0]) == 2, "constructor is MKAverage(m, k)"
    m, k = args[0]
    assert 3 <= m <= 10**5, "3 <= m <= 10^5"
    assert 1 < k * 2 < m, "1 < k*2 < m"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls to addElement and calculateMKAverage"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("addElement", "calculateMKAverage"), (
            "only addElement and calculateMKAverage are called"
        )
        if op == "addElement":
            assert len(a) == 1 and 1 <= a[0] <= 10**5, "1 <= num <= 10^5"
        else:
            assert len(a) == 0, "calculateMKAverage takes no arguments"
