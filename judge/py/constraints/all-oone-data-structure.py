"""All O`one Data Structure: a call sequence on AllOne."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args are parallel"
    assert ops[0] == "AllOne" and args[0] == [], "AllOne() takes no arguments"
    assert len(ops) - 1 <= 5 * 10**4, "At most 5 * 10^4 calls"
    counts: dict[str, int] = {}
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("inc", "dec", "getMaxKey", "getMinKey"), "only inc, dec, getMaxKey, getMinKey"
        if op in ("getMaxKey", "getMinKey"):
            assert len(a) == 0, "getMaxKey and getMinKey take no arguments"
            continue
        assert len(a) == 1 and isinstance(a[0], str), "inc and dec take one key"
        key = a[0]
        assert 1 <= len(key) <= 10, "1 <= key.length <= 10"
        assert all("a" <= c <= "z" for c in key), "key consists of lowercase English letters"
        if op == "inc":
            counts[key] = counts.get(key, 0) + 1
        else:
            assert counts.get(key, 0) > 0, "key exists in the data structure for each dec"
            counts[key] -= 1
