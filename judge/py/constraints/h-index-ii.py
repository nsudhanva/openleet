"""H-Index II: a sorted array of citation counts."""

from itertools import pairwise


def check(citations: list[int]) -> None:
    n = len(citations)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= c <= 1000 for c in citations), "0 <= citations[i] <= 1000"
    assert all(a <= b for a, b in pairwise(citations)), "citations is sorted in ascending order"
