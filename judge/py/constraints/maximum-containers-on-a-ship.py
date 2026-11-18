"""Maximum Containers on a Ship: n x n deck, container weight and max weight."""


def check(n: int, w: int, maxWeight: int) -> None:
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= w <= 1000, "1 <= w <= 1000"
    assert 1 <= maxWeight <= 10**9, "1 <= maxWeight <= 10^9"
