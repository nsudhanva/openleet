"""Satisfiability of Equality Equations: four-character equations like "a==b" or "a!=b"."""


def check(equations: list[str]) -> None:
    assert 1 <= len(equations) <= 500, "1 <= equations.length <= 500"
    for e in equations:
        assert isinstance(e, str) and len(e) == 4, "equations[i].length == 4"
        assert "a" <= e[0] <= "z", "equations[i][0] is a lowercase letter"
        assert e[1] in "=!", "equations[i][1] is either '=' or '!'"
        assert e[2] == "=", "equations[i][2] is '='"
        assert "a" <= e[3] <= "z", "equations[i][3] is a lowercase letter"
