"""Put Marbles in Bags: marble weights and a bag count."""


def check(weights: list[int], k: int) -> None:
    assert isinstance(weights, list), "weights is an array"
    assert 1 <= k <= len(weights) <= 10**5, "1 <= k <= weights.length <= 10^5"
    assert all(1 <= w <= 10**9 for w in weights), "1 <= weights[i] <= 10^9"
