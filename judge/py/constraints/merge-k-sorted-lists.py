"""Merge k Sorted Lists: k ascending linked lists given as value lists."""


def check(lists: list[list[int]]) -> None:
    assert 0 <= len(lists) <= 10**4, "0 <= k <= 10^4"
    assert all(len(x) <= 500 for x in lists), "0 <= lists[i].length <= 500"
    assert sum(len(x) for x in lists) <= 10**4, "sum of lists[i].length <= 10^4"
    for x in lists:
        assert all(-(10**4) <= v <= 10**4 for v in x), "-10^4 <= lists[i][j] <= 10^4"
        assert all(x[i] <= x[i + 1] for i in range(len(x) - 1)), (
            "lists[i] is sorted in ascending order"
        )
