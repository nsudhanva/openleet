"""Two Sum III: TwoSum constructor, add and find calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per operation"
    assert ops[0] == "TwoSum" and args[0] == [], "constructor takes no arguments"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to add and find"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("add", "find") and len(a) == 1, "calls are add(number) and find(value)"
        if op == "add":
            assert -(10**5) <= a[0] <= 10**5, "-10^5 <= number <= 10^5"
        else:
            assert -(2**31) <= a[0] <= 2**31 - 1, "-2^31 <= value <= 2^31 - 1"
