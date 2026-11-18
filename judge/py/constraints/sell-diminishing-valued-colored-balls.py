"""Sell Diminishing-Valued Colored Balls: ball counts per color plus an order count."""


def check(inventory: list[int], orders: int) -> None:
    assert 1 <= len(inventory) <= 10**5, "1 <= inventory.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in inventory), "1 <= inventory[i] <= 10^9"
    assert 1 <= orders <= min(sum(inventory), 10**9), "1 <= orders <= min(sum(inventory[i]), 10^9)"
