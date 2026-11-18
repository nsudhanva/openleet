"""Check for Contradictions in Equations: [A, B] name pairs with A / B = value."""


def check(equations: list[list[str]], values: list[float]) -> None:
    assert isinstance(equations, list) and isinstance(values, list), "equations, values are lists"
    assert 1 <= len(equations) <= 100, "1 <= equations.length <= 100"
    assert all(isinstance(e, list) and len(e) == 2 for e in equations), "equations[i].length == 2"
    assert all(isinstance(x, str) and 1 <= len(x) <= 5 for e in equations for x in e), (
        "1 <= Ai.length, Bi.length <= 5"
    )
    assert all("a" <= c <= "z" for e in equations for x in e for c in x), (
        "Ai, Bi consist of lowercase English letters"
    )
    assert len(equations) == len(values), "equations.length == values.length"
    assert all(0.0 < v <= 10.0 for v in values), "0.0 < values[i] <= 10.0"
    assert all(abs(v * 100 - round(v * 100)) < 1e-6 for v in values), (
        "values[i] has a maximum of 2 decimal places"
    )
