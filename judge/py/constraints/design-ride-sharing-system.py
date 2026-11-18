"""Design Ride Sharing System: RideSharingSystem calls."""


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
        "RideSharingSystem",
        0,
        {"addDriver": 1, "addRider": 1, "cancelRider": 1, "matchDriverWithRider": 0},
    )
    assert len(ops) - 1 <= 1000, "at most 1000 calls"
    riders, drivers = set(), set()
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "matchDriverWithRider":
            continue
        assert isinstance(a[0], int) and 1 <= a[0] <= 1000, "1 <= riderId, driverId <= 1000"
        if op == "addRider":
            assert a[0] not in riders, "each riderId is added at most once"
            riders.add(a[0])
        elif op == "addDriver":
            assert a[0] not in drivers, "each driverId is added at most once"
            drivers.add(a[0])
