"""Next Greater Node In Linked List: a linked list of positive integers."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 10**4, "1 <= n <= 10^4"
    assert all(1 <= v <= 10**9 for v in head), "1 <= Node.val <= 10^9"
