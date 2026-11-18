"""Lemonade Change: a list of bills paid in order."""


def check(bills: list[int]) -> None:
    assert 1 <= len(bills) <= 10**5, "1 <= bills.length <= 10^5"
    assert all(b in (5, 10, 20) for b in bills), "bills[i] is either 5, 10, or 20"
