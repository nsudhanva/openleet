"""Find the Peaks: an array of mountain heights."""


def check(mountain: list[int]) -> None:
    assert 3 <= len(mountain) <= 100, "3 <= mountain.length <= 100"
    assert all(1 <= v <= 100 for v in mountain), "1 <= mountain[i] <= 100"
