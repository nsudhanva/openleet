"""Combination Sum: distinct candidates and a target."""


def check(candidates: list[int], target: int) -> None:
    assert 1 <= len(candidates) <= 30, "1 <= candidates.length <= 30"
    assert all(2 <= c <= 40 for c in candidates), "2 <= candidates[i] <= 40"
    assert len(set(candidates)) == len(candidates), "all elements of candidates are distinct"
    assert 1 <= target <= 40, "1 <= target <= 40"
    ways = [1] + [0] * target
    for c in candidates:
        for t in range(c, target + 1):
            ways[t] += ways[t - c]
    assert ways[target] < 150, "fewer than 150 unique combinations sum to target"
