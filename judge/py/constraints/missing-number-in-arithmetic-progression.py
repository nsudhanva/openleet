"""Missing Number In Arithmetic Progression: a progression with one interior value removed."""

import itertools


def check(arr: list[int]) -> None:
    n = len(arr)
    assert 3 <= n <= 1000, "3 <= arr.length <= 1000"
    assert all(0 <= v <= 10**5 for v in arr), "0 <= arr[i] <= 10^5"
    span = arr[-1] - arr[0]
    assert span % n == 0, (
        "valid array: first and last values bound a progression with one value removed"
    )
    d = span // n
    gaps = [b - a for a, b in itertools.pairwise(arr)]
    doubled = sum(g == 2 * d for g in gaps)
    if d == 0:
        assert all(g == 0 for g in gaps), (
            "valid array: arithmetic progression with one value removed"
        )
    else:
        assert doubled == 1 and sum(g == d for g in gaps) == n - 2, (
            "valid array: arithmetic progression with one interior value removed"
        )
