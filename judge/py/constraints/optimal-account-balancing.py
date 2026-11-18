"""Optimal Account Balancing: a list of [from, to, amount] transactions."""


def check(transactions: list[list[int]]) -> None:
    assert 1 <= len(transactions) <= 8, "1 <= transactions.length <= 8"
    assert all(len(t) == 3 for t in transactions), "transactions[i].length == 3"
    assert all(0 <= t[0] < 12 and 0 <= t[1] < 12 for t in transactions), "0 <= fromi, toi < 12"
    assert all(t[0] != t[1] for t in transactions), "fromi != toi"
    assert all(1 <= t[2] <= 100 for t in transactions), "1 <= amounti <= 100"
