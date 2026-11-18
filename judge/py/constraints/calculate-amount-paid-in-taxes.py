"""Calculate Amount Paid in Taxes: [upper, percent] brackets and an income."""

from itertools import pairwise


def check(brackets: list[list[int]], income: int) -> None:
    assert 1 <= len(brackets) <= 100, "1 <= brackets.length <= 100"
    assert all(len(b) == 2 for b in brackets), "brackets[i].length == 2"
    assert all(1 <= u <= 1000 for u, _ in brackets), "1 <= upperi <= 1000"
    assert all(0 <= p <= 100 for _, p in brackets), "0 <= percenti <= 100"
    assert 0 <= income <= 1000, "0 <= income <= 1000"
    assert all(a[0] < b[0] for a, b in pairwise(brackets)), (
        "upperi is sorted in ascending order and unique"
    )
    assert brackets[-1][0] >= income, "the last upper bound is >= income"
