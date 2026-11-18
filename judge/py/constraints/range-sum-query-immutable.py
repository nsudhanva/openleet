"""Range Sum Query - Immutable: an array, then sumRange calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "NumArray" and len(args[0]) == 1, "constructor takes nums"
    nums = args[0][0]
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to sumRange"
    for op, a in zip(ops[1:], args[1:], strict=False):
        assert op == "sumRange" and len(a) == 2, "only sumRange(left, right) is called"
        assert 0 <= a[0] <= a[1] < len(nums), "0 <= left <= right < nums.length"
