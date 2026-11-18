"""Check if Grid can be Cut into Sections: an n x n grid size and non-overlapping rectangles."""

from bisect import bisect_left


def check(n: int, rectangles: list[list[int]]) -> None:
    assert 3 <= n <= 10**9, "3 <= n <= 10^9"
    assert 3 <= len(rectangles) <= 10**5, "3 <= rectangles.length <= 10^5"
    assert all(len(r) == 4 for r in rectangles), "rectangles[i].length == 4"
    assert all(0 <= r[0] < r[2] <= n for r in rectangles), (
        "0 <= rectangles[i][0] < rectangles[i][2] <= n"
    )
    assert all(0 <= r[1] < r[3] <= n for r in rectangles), (
        "0 <= rectangles[i][1] < rectangles[i][3] <= n"
    )
    events = []
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))
        events.append((x2, 0, y1, y2))
    events.sort()
    starts: list[int] = []
    ends: list[int] = []
    for _, kind, y1, y2 in events:
        if kind == 0:
            i = bisect_left(starts, y1)
            del starts[i]
            del ends[i]
            continue
        i = bisect_left(starts, y1)
        assert i == 0 or ends[i - 1] <= y1, "No two rectangles overlap"
        assert i == len(starts) or starts[i] >= y2, "No two rectangles overlap"
        starts.insert(i, y1)
        ends.insert(i, y2)
