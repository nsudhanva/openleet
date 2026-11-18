"""Alternating Groups I: a circular 0/1 colour array."""


def check(colors: list[int]) -> None:
    assert 3 <= len(colors) <= 100, "3 <= colors.length <= 100"
    assert all(c in (0, 1) for c in colors), "0 <= colors[i] <= 1"
