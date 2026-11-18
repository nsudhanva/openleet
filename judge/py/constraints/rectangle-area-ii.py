"""Rectangle Area II: a list of axis-aligned rectangles [x1, y1, x2, y2] with non-zero area."""


def check(rectangles: list[list[int]]) -> None:
    assert 1 <= len(rectangles) <= 200, "1 <= rectangles.length <= 200"
    assert all(len(r) == 4 for r in rectangles), "rectangles[i].length == 4"
    assert all(0 <= v <= 10**9 for r in rectangles for v in r), "0 <= xi1, yi1, xi2, yi2 <= 10^9"
    assert all(x1 <= x2 and y1 <= y2 for x1, y1, x2, y2 in rectangles), "xi1 <= xi2 and yi1 <= yi2"
    assert all(x1 < x2 and y1 < y2 for x1, y1, x2, y2 in rectangles), (
        "all rectangles have non zero area"
    )
