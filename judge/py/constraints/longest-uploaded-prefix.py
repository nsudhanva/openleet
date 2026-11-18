"""Longest Uploaded Prefix: a design class with upload(video) and longest() calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args line up"
    assert ops[0] == "LUPrefix" and len(args[0]) == 1, "constructor LUPrefix(n)"
    n = args[0][0]
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    calls = ops[1:]
    assert len(calls) <= 2 * 10**5, "at most 2 * 10^5 calls to upload and longest"
    assert any(o == "longest" for o in calls), "at least one call will be made to longest"
    seen = set()
    for op, a in zip(calls, args[1:], strict=True):
        assert op in ("upload", "longest"), "only upload and longest are called"
        if op == "longest":
            assert len(a) == 0, "longest takes no arguments"
        else:
            assert len(a) == 1, "upload takes one argument"
            v = a[0]
            assert 1 <= v <= n, "1 <= video <= n"
            assert v not in seen, "all values of video are distinct"
            seen.add(v)
