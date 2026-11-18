"""Pizza With 3n Slices: a circular list of slice sizes whose length is a multiple of 3."""


def check(slices: list[int]) -> None:
    assert 1 <= len(slices) <= 500, "1 <= slices.length <= 500"
    assert len(slices) % 3 == 0, "3 * n == slices.length"
    assert all(1 <= v <= 1000 for v in slices), "1 <= slices[i] <= 1000"
