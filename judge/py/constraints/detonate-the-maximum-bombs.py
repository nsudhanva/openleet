"""Detonate the Maximum Bombs: a list of [x, y, radius] bombs."""


def check(bombs: list[list[int]]) -> None:
    assert 1 <= len(bombs) <= 100, "1 <= bombs.length <= 100"
    assert all(len(b) == 3 for b in bombs), "bombs[i].length == 3"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for b in bombs for v in b), (
        "1 <= xi, yi, ri <= 10^5"
    )
