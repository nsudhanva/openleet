"""Walking Robot Simulation II: Robot(width, height) then step/getPos/getDir calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have the same length"
    assert ops[0] == "Robot", "the first call is the constructor"
    assert len(args[0]) == 2, "Robot takes width and height"
    width, height = args[0]
    assert 2 <= width <= 100 and 2 <= height <= 100, "2 <= width, height <= 100"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls in total"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("step", "getPos", "getDir"), "calls are step, getPos, getDir"
        if op == "step":
            assert len(a) == 1 and 1 <= a[0] <= 10**5, "1 <= num <= 10^5"
        else:
            assert len(a) == 0, "getPos and getDir take no arguments"
