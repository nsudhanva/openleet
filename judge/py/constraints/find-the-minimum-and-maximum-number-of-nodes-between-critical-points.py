"""Find the Minimum and Maximum Number of Nodes Between Critical Points: a linked list of values."""


def check(head: list[int]) -> None:
    assert 2 <= len(head) <= 10**5, "number of nodes in [2, 10^5]"
    assert all(1 <= v <= 10**5 for v in head), "1 <= Node.val <= 10^5"
