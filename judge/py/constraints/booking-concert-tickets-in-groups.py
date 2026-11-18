"""Booking Concert Tickets in Groups: BookMyShow(n, m) followed by gather and scatter calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "BookMyShow" and len(args[0]) == 2, "BookMyShow(n, m) is called first"
    n, m = args[0]
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert 1 <= m <= 10**9, "1 <= m <= 10^9"
    assert len(ops) - 1 <= 5 * 10**4, "at most 5 * 10^4 calls in total to gather and scatter"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("gather", "scatter"), "only gather and scatter are called"
        assert len(a) == 2, "gather and scatter take (k, maxRow)"
        k, max_row = a
        assert 1 <= k <= 10**9, "1 <= k <= 10^9"
        assert 0 <= max_row <= n - 1, "0 <= maxRow <= n - 1"
