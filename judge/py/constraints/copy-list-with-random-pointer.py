"""Copy List with Random Pointer: a list of [value, random index or None] pairs."""


def check(head: list) -> None:
    assert isinstance(head, list), "head is a list of nodes"
    assert 0 <= len(head) <= 1000, "0 <= n <= 1000"
    assert all(isinstance(p, list) and len(p) == 2 for p in head), (
        "each node is [val, random_index]"
    )
    assert all(isinstance(p[0], int) for p in head), "Node.val is an integer"
    assert all(-(10**4) <= p[0] <= 10**4 for p in head), "-10^4 <= Node.val <= 10^4"
    n = len(head)
    assert all(p[1] is None or (isinstance(p[1], int) and 0 <= p[1] < n) for p in head), (
        "Node.random is null or is pointing to some node in the linked list"
    )
