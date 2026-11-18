"""Remove Duplicates From an Unsorted Linked List: a linked list as a list of values."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(1 <= v <= 10**5 for v in head), "1 <= Node.val <= 10^5"
