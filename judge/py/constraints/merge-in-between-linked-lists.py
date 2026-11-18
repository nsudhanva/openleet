"""Merge In Between Linked Lists: two linked lists (value lists) and indices a, b."""


def check(list1: list[int], a: int, b: int, list2: list[int]) -> None:
    assert 3 <= len(list1) <= 10**4, "3 <= list1.length <= 10^4"
    assert 1 <= a <= b < len(list1) - 1, "1 <= a <= b < list1.length - 1"
    assert 1 <= len(list2) <= 10**4, "1 <= list2.length <= 10^4"
