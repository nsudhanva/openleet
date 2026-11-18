"""Find Median from Data Stream: MedianFinder() then addNum(num) and findMedian() calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "MedianFinder" and args[0] == [], "constructor takes no arguments"
    assert len(ops) - 1 <= 5 * 10**4, "at most 5 * 10^4 calls to addNum and findMedian"
    count = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "addNum":
            assert len(a) == 1, "addNum takes one argument"
            assert -(10**5) <= a[0] <= 10**5, "-10^5 <= num <= 10^5"
            count += 1
        else:
            assert op == "findMedian" and a == [], "calls are addNum or findMedian"
            assert count >= 1, "at least one element before calling findMedian"
