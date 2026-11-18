"""Card Flipping Game: fronts and backs of n cards."""


def check(fronts: list[int], backs: list[int]) -> None:
    assert isinstance(fronts, list) and isinstance(backs, list), "fronts, backs are lists"
    n = len(fronts)
    assert n == len(backs), "n == fronts.length == backs.length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(1 <= v <= 2000 for v in fronts), "1 <= fronts[i] <= 2000"
    assert all(1 <= v <= 2000 for v in backs), "1 <= backs[i] <= 2000"
