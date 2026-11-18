"""Maximum Frequency Stack: calls to FreqStack, push and pop."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per call"
    assert ops[0] == "FreqStack" and args[0] == [], "FreqStack() takes no arguments"
    assert len(ops) - 1 <= 2 * 10**4, "at most 2 * 10^4 calls to push and pop"
    size = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "push":
            assert len(a) == 1 and isinstance(a[0], int), "push takes one integer"
            assert 0 <= a[0] <= 10**9, "0 <= val <= 10^9"
            size += 1
        else:
            assert op == "pop" and a == [], "calls are push(val) or pop()"
            assert size > 0, "at least one element in the stack before pop"
            size -= 1
