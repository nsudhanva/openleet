"""Number of Ways to Reach a Position After Exactly k Steps: start, end and step count."""


def check(startPos: int, endPos: int, k: int) -> None:
    assert all(isinstance(v, int) for v in (startPos, endPos, k)), "integers"
    assert 1 <= startPos <= 1000, "1 <= startPos <= 1000"
    assert 1 <= endPos <= 1000, "1 <= endPos <= 1000"
    assert 1 <= k <= 1000, "1 <= k <= 1000"
