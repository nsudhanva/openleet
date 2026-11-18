"""Dinner Plate Stacks: a DinnerPlates design with push, pop and popAtStack calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == "DinnerPlates", "first operation is the constructor"
    assert len(args[0]) == 1 and isinstance(args[0][0], int), "constructor takes capacity"
    assert 1 <= args[0][0] <= 2 * 10**4, "1 <= capacity <= 2 * 10^4"
    assert len(ops) - 1 <= 2 * 10**5, "at most 2 * 10^5 calls"
    arity = {"push": 1, "pop": 0, "popAtStack": 1}
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in arity, "only push, pop and popAtStack are called"
        assert len(a) == arity[op], "argument count matches the method"
        if op == "push":
            assert isinstance(a[0], int) and 1 <= a[0] <= 2 * 10**4, "1 <= val <= 2 * 10^4"
        elif op == "popAtStack":
            assert isinstance(a[0], int) and 0 <= a[0] <= 10**5, "0 <= index <= 10^5"
