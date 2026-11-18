"""Max Stack: MaxStack operations and their arguments."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per call"
    assert ops[0] == "MaxStack" and args[0] == [], "constructor takes no arguments"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls"
    size = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "push":
            assert len(a) == 1, "push takes one argument"
            assert -(10**7) <= a[0] <= 10**7, "-10^7 <= x <= 10^7"
            size += 1
        else:
            assert op in ("pop", "top", "peekMax", "popMax"), "known operation"
            assert a == [], "no arguments"
            assert size >= 1, "stack is non-empty when pop, top, peekMax, or popMax is called"
            if op in ("pop", "popMax"):
                size -= 1
