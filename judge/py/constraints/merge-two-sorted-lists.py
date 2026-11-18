"""Merge Two Sorted Lists: two linked lists (value lists) sorted in non-decreasing order."""


def check(list1: list[int], list2: list[int]) -> None:
    for x in (list1, list2):
        assert len(x) <= 50, "number of nodes in [0, 50]"
        assert all(-100 <= v <= 100 for v in x), "-100 <= Node.val <= 100"
        assert all(x[i] <= x[i + 1] for i in range(len(x) - 1)), "sorted in non-decreasing order"
