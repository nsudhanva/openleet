"""Design Linked List: MyLinkedList calls."""


def _shape(ops, args, ctor, ctor_arity, sig):
    assert isinstance(ops, list) and isinstance(args, list), "ops and args are lists"
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == ctor, "first operation is the constructor"
    assert all(isinstance(a, list) for a in args), "each args[i] is a list"
    assert len(args[0]) == ctor_arity, "constructor argument count"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in sig, "known method name"
        assert len(a) == sig[op], "argument count of " + op


def check(ops: list[str], args: list[list]) -> None:
    _shape(
        ops,
        args,
        "MyLinkedList",
        0,
        {"addAtHead": 1, "addAtTail": 1, "addAtIndex": 2, "deleteAtIndex": 1, "get": 1},
    )
    assert len(ops) - 1 <= 2000, "at most 2000 calls"
    for a in args[1:]:
        assert all(isinstance(x, int) and 0 <= x <= 1000 for x in a), "0 <= index, val <= 1000"
