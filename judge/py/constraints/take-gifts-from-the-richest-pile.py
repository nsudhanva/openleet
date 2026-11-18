"""Take Gifts From the Richest Pile: pile sizes and a number of seconds k."""


def check(gifts: list[int], k: int) -> None:
    assert 1 <= len(gifts) <= 10**3, "1 <= gifts.length <= 10^3"
    assert all(1 <= g <= 10**9 for g in gifts), "1 <= gifts[i] <= 10^9"
    assert 1 <= k <= 10**3, "1 <= k <= 10^3"
