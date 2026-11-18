"""Logger Rate Limiter: a constructor call followed by shouldPrintMessage calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "one argument list per operation"
    assert ops[0] == "Logger" and args[0] == [], "the first operation is Logger()"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to shouldPrintMessage"
    prev = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "shouldPrintMessage", "only shouldPrintMessage is called"
        assert len(a) == 2, "shouldPrintMessage(timestamp, message)"
        t, m = a
        assert 0 <= t <= 10**9, "0 <= timestamp <= 10^9"
        assert t >= prev, "timestamps are passed in non-decreasing order"
        prev = t
        assert isinstance(m, str) and 1 <= len(m) <= 30, "1 <= message.length <= 30"
