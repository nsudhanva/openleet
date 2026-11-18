"""Longest Common Subsequence Between Sorted Arrays: a list of strictly increasing int arrays."""


def check(arrays: list[list[int]]) -> None:
    assert 2 <= len(arrays) <= 100, "2 <= arrays.length <= 100"
    assert all(isinstance(a, list) for a in arrays), "arrays[i] is an array"
    assert all(1 <= len(a) <= 100 for a in arrays), "1 <= arrays[i].length <= 100"
    assert all(1 <= v <= 100 for a in arrays for v in a), "1 <= arrays[i][j] <= 100"
    assert all(all(a[j] < a[j + 1] for j in range(len(a) - 1)) for a in arrays), (
        "arrays[i] is sorted in strictly increasing order"
    )
