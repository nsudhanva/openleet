"""Minimum Money Required Before Transactions: [cost, cashback] pairs."""


def check(transactions: list[list[int]]) -> None:
    assert 1 <= len(transactions) <= 10**5, "1 <= transactions.length <= 10^5"
    assert all(len(t) == 2 for t in transactions), "transactions[i].length == 2"
    assert all(0 <= c <= 10**9 and 0 <= b <= 10**9 for c, b in transactions), (
        "0 <= cost_i, cashback_i <= 10^9"
    )
