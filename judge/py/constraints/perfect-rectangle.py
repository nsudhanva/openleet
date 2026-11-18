"""Perfect Rectangle: axis-aligned rectangles as [x, y, a, b]."""


def check(rectangles: list[list[int]]) -> None:
    assert 1 <= len(rectangles) <= 2 * 10**4, "1 <= rectangles.length <= 2 * 10^4"
    assert all(len(r) == 4 for r in rectangles), "rectangles[i].length == 4"
    assert all(-(10**5) <= x < a <= 10**5 for x, _, a, _ in rectangles), "-10^5 <= xi < ai <= 10^5"
    assert all(-(10**5) <= y < b <= 10**5 for _, y, _, b in rectangles), "-10^5 <= yi < bi <= 10^5"
