"""Design Spreadsheet: constructor and calls of a 26-column spreadsheet."""

import re


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert len(args[0]) == 1 and isinstance(args[0][0], int), "Spreadsheet(rows)"
    rows = args[0][0]
    assert 1 <= rows <= 10**3, "1 <= rows <= 10^3"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls"

    def ref(s) -> None:
        assert isinstance(s, str) and re.fullmatch(r"[A-Z][0-9]+", s), (
            "cell is a letter A-Z and a row"
        )
        assert 1 <= int(s[1:]) <= rows, "row number between 1 and rows"

    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "setCell":
            assert len(a) == 2, "setCell(cell, value)"
            ref(a[0])
            assert isinstance(a[1], int) and 0 <= a[1] <= 10**5, "0 <= value <= 10^5"
        elif op == "resetCell":
            assert len(a) == 1, "resetCell(cell)"
            ref(a[0])
        elif op == "getValue":
            assert len(a) == 1 and isinstance(a[0], str), "getValue(formula)"
            assert a[0].startswith("=") and a[0].count("+") == 1, 'formula is "=X+Y"'
            for part in a[0][1:].split("+"):
                if part.isdigit():
                    assert int(part) <= 10**5, "integers in a formula are <= 10^5"
                else:
                    ref(part)
        else:
            raise AssertionError("unknown operation")
