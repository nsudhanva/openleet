"""Stock Price Fluctuation: calls to update, current, maximum and minimum."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have one entry per call"
    assert ops[0] == "StockPrice" and args[0] == [], "StockPrice() takes no arguments"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls"
    updated = False
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "update":
            assert len(a) == 2, "update(timestamp, price)"
            assert 1 <= a[0] <= 10**9 and 1 <= a[1] <= 10**9, "1 <= timestamp, price <= 10^9"
            updated = True
        else:
            assert op in ("current", "maximum", "minimum"), (
                "calls are update, current, maximum, minimum"
            )
            assert a == [], f"{op}() takes no arguments"
            assert updated, "current, maximum, minimum are called only after update"
