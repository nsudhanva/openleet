"""Implement Queue using Stacks: calls on a MyQueue."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops and ops[0] == "MyQueue", "constructor first"
    assert args[0] == [], "MyQueue() takes no arguments"
    assert len(ops) - 1 <= 100, "At most 100 calls will be made to push, pop, peek, and empty"
    size = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "push":
            assert len(a) == 1 and 1 <= a[0] <= 9, "1 <= x <= 9"
            size += 1
        else:
            assert op in ("pop", "peek", "empty"), "only push, pop, peek, empty are called"
            assert a == [], f"{op} takes no arguments"
            if op == "pop":
                assert size > 0, "All the calls to pop and peek are valid"
                size -= 1
            elif op == "peek":
                assert size > 0, "All the calls to pop and peek are valid"
