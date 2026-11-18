"""Merge Nodes in Between Zeros: a linked list (value list) of zero-separated segments."""


def check(head: list[int]) -> None:
    assert 3 <= len(head) <= 2 * 10**5, "number of nodes in [3, 2 * 10^5]"
    assert all(0 <= v <= 1000 for v in head), "0 <= Node.val <= 1000"
    assert all(not (head[i] == 0 and head[i + 1] == 0) for i in range(len(head) - 1)), (
        "no two consecutive zeros"
    )
    assert head[0] == 0 and head[-1] == 0, "list begins and ends with 0"
