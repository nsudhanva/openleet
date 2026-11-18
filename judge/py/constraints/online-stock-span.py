"""Online Stock Span: a design class StockSpanner with next(price) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "StockSpanner" and all(o == "next" for o in ops[1:]), (
        "a constructor call followed by next calls"
    )
    assert args[0] == [], "constructor takes no arguments"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls will be made to next"
    for a in args[1:]:
        assert len(a) == 1, "next takes one argument"
        assert 1 <= a[0] <= 10**5, "1 <= price <= 10^5"
