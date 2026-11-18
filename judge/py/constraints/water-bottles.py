"""Water Bottles: a bottle count and an exchange rate."""


def check(numBottles: int, numExchange: int) -> None:
    assert 1 <= numBottles <= 100, "1 <= numBottles <= 100"
    assert 2 <= numExchange <= 100, "2 <= numExchange <= 100"
