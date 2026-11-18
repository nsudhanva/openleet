"""Flatten 2D Vector: calls on Vector2D, built from a list of integer lists."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "one argument list per call"
    assert ops[0] == "Vector2D" and len(args[0]) == 1, "constructor is Vector2D(vec)"
    vec = args[0][0]
    assert 0 <= len(vec) <= 200, "0 <= vec.length <= 200"
    assert all(0 <= len(row) <= 500 for row in vec), "0 <= vec[i].length <= 500"
    assert all(-500 <= v <= 500 for row in vec for v in row), "-500 <= vec[i][j] <= 500"
    assert len(ops) - 1 <= 10**5, "at most 10^5 calls to next and hasNext"
    remaining = sum(len(row) for row in vec)
    for op in ops[1:]:
        assert op in ("next", "hasNext"), "only next and hasNext are called"
        if op == "next":
            assert remaining > 0, "all the calls to next are valid"
            remaining -= 1
