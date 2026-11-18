"""Detect Squares: add/count calls on points of a plane."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert args[0] == [], "DetectSquares()"
    assert len(ops) - 1 <= 3000, "at most 3000 calls to add and count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("add", "count"), "unknown operation"
        assert len(a) == 1 and isinstance(a[0], list), f"{op}(point)"
        p = a[0]
        assert len(p) == 2, "point.length == 2"
        assert all(isinstance(v, int) and 0 <= v <= 1000 for v in p), "0 <= x, y <= 1000"
