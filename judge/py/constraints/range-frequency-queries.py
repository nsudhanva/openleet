"""Range Frequency Queries: an array, then query(left, right, value) calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "RangeFreqQuery" and len(args[0]) == 1, "constructor takes arr"
    arr = args[0][0]
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in arr), "1 <= arr[i] <= 10^4"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls to query"
    for op, a in zip(ops[1:], args[1:], strict=False):
        assert op == "query" and len(a) == 3, "only query(left, right, value) is called"
        left, right, value = a
        assert 1 <= value <= 10**4, "1 <= value <= 10^4"
        assert 0 <= left <= right < len(arr), "0 <= left <= right < arr.length"
