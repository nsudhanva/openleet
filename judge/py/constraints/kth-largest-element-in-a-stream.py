"""Kth Largest Element in a Stream: a design problem with KthLargest(k, nums) and add(val) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "KthLargest" and len(args[0]) == 2, "constructor KthLargest(k, nums)"
    k, nums = args[0]
    assert 0 <= len(nums) <= 10**4, "0 <= nums.length <= 10^4"
    assert 1 <= k <= len(nums) + 1, "1 <= k <= nums.length + 1"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to add"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "add" and len(a) == 1, "calls are add(val)"
        assert -(10**4) <= a[0] <= 10**4, "-10^4 <= val <= 10^4"
