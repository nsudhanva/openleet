"""Design SQL: table names and column counts, then ins/rmv/sel/exp calls."""

import re


def _word(s) -> bool:
    return isinstance(s, str) and re.fullmatch(r"[a-z]{1,10}", s) is not None


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert len(args[0]) == 2, "SQL(names, columns)"
    names, columns = args[0]
    assert isinstance(names, list) and isinstance(columns, list), "names and columns are lists"
    assert len(names) == len(columns), "n == names.length == columns.length"
    assert 1 <= len(names) <= 10**4, "1 <= n <= 10^4"
    assert all(_word(s) for s in names), "names[i] has 1..10 lowercase letters"
    assert all(isinstance(c, int) and 1 <= c <= 10 for c in columns), "1 <= columns[i] <= 10"
    assert len(set(names)) == len(names), "all names[i] are distinct"
    count = {"ins": 0, "rmv": 0, "sel": 0, "exp": 0}
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in count, "unknown operation"
        count[op] += 1
        assert a and _word(a[0]), "name has 1..10 lowercase letters"
        if op == "ins":
            assert len(a) == 2 and isinstance(a[1], list), "ins(name, row)"
            assert 1 <= len(a[1]) <= 10, "1 <= row.length <= 10"
            assert all(_word(s) for s in a[1]), "row[i] has 1..10 lowercase letters"
        elif op == "rmv":
            assert len(a) == 2 and isinstance(a[1], int), "rmv(name, rowId)"
        elif op == "sel":
            assert len(a) == 3 and all(isinstance(x, int) for x in a[1:]), (
                "sel(name, rowId, columnId)"
            )
        else:
            assert len(a) == 1, "exp(name)"
    assert count["ins"] + count["rmv"] <= 2000, "at most 2000 calls to ins and rmv"
    assert count["sel"] <= 10**4, "at most 10^4 calls to sel"
    assert count["exp"] <= 500, "at most 500 calls to exp"
