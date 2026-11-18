"""Combination Sum II: candidate numbers and a target."""


def check(candidates: list[int], target: int) -> None:
    assert 1 <= len(candidates) <= 100, "1 <= candidates.length <= 100"
    assert all(1 <= c <= 50 for c in candidates), "1 <= candidates[i] <= 50"
    assert 1 <= target <= 30, "1 <= target <= 30"
