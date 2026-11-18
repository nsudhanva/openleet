"""Maximum Distance in Arrays: m sorted arrays of integers."""

from itertools import pairwise


def check(arrays: list[list[int]]) -> None:
    assert 2 <= len(arrays) <= 10**5, "2 <= m <= 10^5"
    assert all(1 <= len(a) <= 500 for a in arrays), "1 <= arrays[i].length <= 500"
    assert sum(len(a) for a in arrays) <= 10**5, "at most 10^5 integers in all the arrays"
    assert all(-(10**4) <= v <= 10**4 for a in arrays for v in a), "-10^4 <= arrays[i][j] <= 10^4"
    assert all(x <= y for a in arrays for x, y in pairwise(a)), (
        "arrays[i] is sorted in ascending order"
    )
