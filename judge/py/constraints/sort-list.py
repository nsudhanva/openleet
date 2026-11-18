"""Sort List: a linked list of integers, given as a list of values."""


def check(head: list[int]) -> None:
    assert 0 <= len(head) <= 5 * 10**4, "number of nodes in [0, 5 * 10^4]"
    assert all(isinstance(v, int) and -(10**5) <= v <= 10**5 for v in head), (
        "-10^5 <= Node.val <= 10^5"
    )
