"""First Unique Number: calls on FirstUnique, built from an initial queue."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per call"
    assert ops[0] == "FirstUnique" and len(args[0]) == 1, "constructor is FirstUnique(nums)"
    nums = args[0][0]
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**8 for v in nums), "1 <= nums[i] <= 10^8"
    assert len(ops) - 1 <= 50000, "at most 50000 calls to showFirstUnique and add"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("showFirstUnique", "add"), "only showFirstUnique and add are called"
        if op == "add":
            assert len(a) == 1 and 1 <= a[0] <= 10**8, "1 <= value <= 10^8"
        else:
            assert len(a) == 0, "showFirstUnique takes no arguments"
