"""Build a Matrix With Conditions: k and row/column ordering pairs."""


def check(k: int, rowConditions: list[list[int]], colConditions: list[list[int]]) -> None:
    assert 2 <= k <= 400, "2 <= k <= 400"
    for name, conds in (("rowConditions", rowConditions), ("colConditions", colConditions)):
        assert 1 <= len(conds) <= 10**4, f"1 <= {name}.length <= 10^4"
        assert all(len(c) == 2 for c in conds), f"{name}[i].length == 2"
        assert all(1 <= a <= k and 1 <= b <= k for a, b in conds), f"1 <= {name} values <= k"
        assert all(a != b for a, b in conds), f"{name}: first != second"
