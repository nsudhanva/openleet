"""Maximum Area of Longest Diagonal Rectangle: a list of [length, width] pairs."""


def check(dimensions: list[list[int]]) -> None:
    assert 1 <= len(dimensions) <= 100, "1 <= dimensions.length <= 100"
    assert all(len(d) == 2 for d in dimensions), "dimensions[i].length == 2"
    assert all(1 <= v <= 100 for d in dimensions for v in d), (
        "1 <= dimensions[i][0], dimensions[i][1] <= 100"
    )
