"""Maximum Number of Darts Inside of a Circular Dartboard: unique [x, y] points and a radius."""


def check(darts: list[list[int]], r: int) -> None:
    assert 1 <= len(darts) <= 100, "1 <= darts.length <= 100"
    assert all(len(d) == 2 for d in darts), "darts[i].length == 2"
    assert all(-(10**4) <= v <= 10**4 for d in darts for v in d), "-10^4 <= xi, yi <= 10^4"
    assert len({tuple(d) for d in darts}) == len(darts), "all the darts are unique"
    assert 1 <= r <= 5000, "1 <= r <= 5000"
