"""Min Stack: operation names and argument lists for a MinStack."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args align"
    assert ops[0] == "MinStack" and args[0] == [], "constructor takes no arguments"
    calls = ops[1:]
    assert len(calls) <= 3 * 10**4, "at most 3 * 10^4 calls"
    size = 0
    for op, a in zip(calls, args[1:], strict=True):
        if op == "push":
            assert len(a) == 1 and isinstance(a[0], int), "push takes one integer"
            assert -(2**31) <= a[0] <= 2**31 - 1, "-2^31 <= val <= 2^31 - 1"
            size += 1
        else:
            assert op in ("pop", "top", "getMin"), "known method"
            assert a == [], "no arguments"
            assert size > 0, "pop, top and getMin are called on non-empty stacks"
            if op == "pop":
                size -= 1
