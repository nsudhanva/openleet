"""Minimum Jumps to Reach Home: forbidden positions, forward jump a, backward jump b, home x."""


def check(forbidden: list[int], a: int, b: int, x: int) -> None:
    assert 1 <= len(forbidden) <= 1000, "1 <= forbidden.length <= 1000"
    assert 1 <= a <= 2000, "1 <= a <= 2000"
    assert 1 <= b <= 2000, "1 <= b <= 2000"
    assert all(1 <= f <= 2000 for f in forbidden), "1 <= forbidden[i] <= 2000"
    assert 0 <= x <= 2000, "0 <= x <= 2000"
    assert len(set(forbidden)) == len(forbidden), "All the elements in forbidden are distinct"
    assert x not in set(forbidden), "Position x is not forbidden"
