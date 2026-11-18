"""Number of Pairs of Interchangeable Rectangles: a list of [width, height] rectangles."""


def check(rectangles: list[list[int]]) -> None:
    assert 1 <= len(rectangles) <= 10**5, "1 <= n <= 10^5"
    assert all(len(r) == 2 for r in rectangles), "rectangles[i].length == 2"
    assert all(1 <= w <= 10**5 and 1 <= h <= 10**5 for w, h in rectangles), (
        "1 <= widthi, heighti <= 10^5"
    )
