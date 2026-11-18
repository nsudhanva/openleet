"""Evaluate Division: variable-pair equations with values, and queries."""

_ALNUM = set("abcdefghijklmnopqrstuvwxyz0123456789")


def _ok_name(x: str) -> bool:
    return isinstance(x, str) and 1 <= len(x) <= 5 and all(c in _ALNUM for c in x)


def check(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> None:
    assert 1 <= len(equations) <= 20, "1 <= equations.length <= 20"
    assert all(isinstance(e, list) and len(e) == 2 for e in equations), "equations[i].length == 2"
    assert len(values) == len(equations), "values.length == equations.length"
    assert 1 <= len(queries) <= 20, "1 <= queries.length <= 20"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(_ok_name(x) for e in equations for x in e), (
        "1 <= Ai.length, Bi.length <= 5, lower case letters and digits"
    )
    assert all(_ok_name(x) for q in queries for x in q), (
        "1 <= Cj.length, Dj.length <= 5, lower case letters and digits"
    )
    assert all(isinstance(v, (int, float)) and 0.0 < v <= 20.0 for v in values), (
        "0.0 < values[i] <= 20.0"
    )
    # No contradiction: weighted union-find, weight[x] = x / parent[x].
    parent: dict[str, str] = {}
    weight: dict[str, float] = {}

    def find(x: str) -> str:
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        acc = 1.0
        for node in reversed(path):
            acc *= weight[node]
            weight[node] = acc
            parent[node] = x
        return x

    for (a, b), v in zip(equations, values, strict=True):
        for x in (a, b):
            if x not in parent:
                parent[x] = x
                weight[x] = 1.0
        ra, rb = find(a), find(b)
        if ra == rb:
            got = weight[a] / weight[b]
            assert abs(got - v) <= 1e-4 * max(1.0, abs(v)), "there is no contradiction"
        else:
            parent[ra] = rb
            weight[ra] = v * weight[b] / weight[a]
