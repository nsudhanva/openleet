"""Two Sum II: a sorted integer array and a target with exactly one solution."""

from collections import Counter
from itertools import pairwise


def check(numbers: list[int], target: int) -> None:
    assert 2 <= len(numbers) <= 3 * 10**4, "2 <= numbers.length <= 3 * 10^4"
    assert all(-1000 <= v <= 1000 for v in numbers), "-1000 <= numbers[i] <= 1000"
    assert all(a <= b for a, b in pairwise(numbers)), "numbers is sorted in non-decreasing order"
    assert -1000 <= target <= 1000, "-1000 <= target <= 1000"
    c = Counter(numbers)
    pairs = 0
    for v, k in c.items():
        w = target - v
        if v < w:
            pairs += k * c.get(w, 0)
        elif v == w:
            pairs += k * (k - 1) // 2
    assert pairs == 1, "exactly one solution"
