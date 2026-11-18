"""Finding Pairs With a Certain Sum: calls on FindSumPairs, built from two arrays."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per call"
    assert ops[0] == "FindSumPairs" and len(args[0]) == 2, (
        "constructor is FindSumPairs(nums1, nums2)"
    )
    nums1, nums2 = args[0]
    assert 1 <= len(nums1) <= 1000, "1 <= nums1.length <= 1000"
    assert 1 <= len(nums2) <= 10**5, "1 <= nums2.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums1), "1 <= nums1[i] <= 10^9"
    assert all(1 <= v <= 10**5 for v in nums2), "1 <= nums2[i] <= 10^5"
    adds = counts = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("add", "count"), "only add and count are called"
        if op == "add":
            adds += 1
            assert len(a) == 2, "add(index, val)"
            assert 0 <= a[0] < len(nums2), "0 <= index < nums2.length"
            assert 1 <= a[1] <= 10**5, "1 <= val <= 10^5"
        else:
            counts += 1
            assert len(a) == 1 and 1 <= a[0] <= 10**9, "1 <= tot <= 10^9"
    assert adds <= 1000 and counts <= 1000, "at most 1000 calls to add and count each"
