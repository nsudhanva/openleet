"""Distribute Money to Maximum Children: an amount of money and a number of children."""


def check(money: int, children: int) -> None:
    assert 1 <= money <= 200, "1 <= money <= 200"
    assert 2 <= children <= 30, "2 <= children <= 30"
