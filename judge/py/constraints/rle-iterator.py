"""RLE Iterator: a run-length encoding followed by calls to next(n)."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "RLEIterator", "the first operation is the constructor"
    assert len(args[0]) == 1, "the constructor takes encoding"
    encoding = args[0][0]
    assert isinstance(encoding, list), "encoding is a list"
    assert 2 <= len(encoding) <= 1000, "2 <= encoding.length <= 1000"
    assert len(encoding) % 2 == 0, "encoding.length is even"
    assert all(0 <= v <= 10**9 for v in encoding), "0 <= encoding[i] <= 10^9"
    assert len(ops) - 1 <= 1000, "at most 1000 calls will be made to next"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "next", "only next is called"
        assert len(a) == 1, "next takes n"
        assert 1 <= a[0] <= 10**9, "1 <= n <= 10^9"
