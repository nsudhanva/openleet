"""Spiral Matrix IV: matrix size and a linked list (list of values) to fill it."""


def check(m: int, n: int, head: list[int]) -> None:
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert 1 <= len(head) <= m * n, "number of nodes in [1, m * n]"
    assert all(isinstance(v, int) and 0 <= v <= 1000 for v in head), "0 <= Node.val <= 1000"
