"""Range Sum Query - Mutable: an array, then sumRange and update calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "NumArray" and len(args[0]) == 1, "constructor takes nums"
    nums = args[0][0]
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
    assert len(ops) - 1 <= 3 * 10**4, "at most 3 * 10^4 calls"
    for op, a in zip(ops[1:], args[1:], strict=False):
        if op == "sumRange":
            assert len(a) == 2, "sumRange(left, right)"
            assert 0 <= a[0] <= a[1] < len(nums), "0 <= left <= right < nums.length"
        else:
            assert op == "update" and len(a) == 2, "only sumRange and update are called"
            assert 0 <= a[0] < len(nums), "0 <= index < nums.length"
            assert -100 <= a[1] <= 100, "-100 <= val <= 100"
