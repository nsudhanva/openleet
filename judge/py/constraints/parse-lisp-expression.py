"""Parse Lisp Expression: a legal let/add/mult expression whose values fit in 32 bits."""

import sys

LO, HI = -(2**31), 2**31 - 1
RESERVED = {"add", "let", "mult"}


def _is_int(tok: str) -> bool:
    body = tok[1:] if tok[:1] == "-" else tok
    return body.isascii() and body.isdigit()


def _is_var(tok: str) -> bool:
    return (
        bool(tok)
        and "a" <= tok[0] <= "z"
        and all("a" <= c <= "z" or "0" <= c <= "9" for c in tok)
        and tok not in RESERVED
    )


def check(expression: str) -> None:
    assert isinstance(expression, str), "expression is a string"
    assert 1 <= len(expression) <= 2000, "1 <= expression.length <= 2000"
    assert expression == expression.strip(" "), "no leading or trailing spaces"
    assert "  " not in expression, "all tokens are separated by a single space"
    assert all(
        c in "()- " or (c.isascii() and c.isalnum() and (c.islower() or c.isdigit()))
        for c in expression
    ), "expression uses lowercase letters, digits, '-', spaces and parentheses"
    toks = expression.replace("(", " ( ").replace(")", " ) ").split()
    pos = 0

    def num(v: int) -> int:
        assert LO <= v <= HI, "all intermediate calculations fit in a 32-bit integer"
        return v

    def ev(scope: dict) -> int:
        nonlocal pos
        assert pos < len(toks), "the expression is legal"
        t = toks[pos]
        if t != "(":
            pos += 1
            if _is_int(t):
                return num(int(t))
            assert _is_var(t) and t in scope, (
                "every variable is defined and the expression is legal"
            )
            return scope[t]
        pos += 1
        assert pos < len(toks), "the expression is legal"
        op = toks[pos]
        pos += 1
        if op in ("add", "mult"):
            a = ev(scope)
            b = ev(scope)
            r = num(a + b if op == "add" else a * b)
        else:
            assert op == "let", "the expression is legal"
            inner = dict(scope)
            while True:
                assert pos < len(toks), "the expression is legal"
                if (
                    toks[pos] != "("
                    and _is_var(toks[pos])
                    and pos + 1 < len(toks)
                    and toks[pos + 1] != ")"
                ):
                    name = toks[pos]
                    pos += 1
                    inner[name] = ev(inner)
                else:
                    r = ev(inner)
                    break
        assert pos < len(toks) and toks[pos] == ")", "the expression is legal"
        pos += 1
        return r

    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10000))
    try:
        ev({})
    finally:
        sys.setrecursionlimit(old)
    assert pos == len(toks), "the expression is legal"
