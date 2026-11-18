"""Maximum Twin Sum of a Linked List: a linked list of positive values, as a list."""


def check(head: list[int]) -> None:
    assert 2 <= len(head) <= 10**5, "number of nodes in [2, 10^5]"
    assert len(head) % 2 == 0, "the number of nodes is even"
    assert all(1 <= v <= 10**5 for v in head), "1 <= Node.val <= 10^5"
