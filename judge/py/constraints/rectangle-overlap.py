"""Rectangle Overlap: two axis-aligned rectangles [x1, y1, x2, y2] with non-zero area."""


def check(rec1: list[int], rec2: list[int]) -> None:
    assert len(rec1) == 4, "rec1.length == 4"
    assert len(rec2) == 4, "rec2.length == 4"
    assert all(-(10**9) <= v <= 10**9 for v in rec1 + rec2), "-10^9 <= rec1[i], rec2[i] <= 10^9"
    for rec in (rec1, rec2):
        assert rec[0] < rec[2] and rec[1] < rec[3], (
            "rec1 and rec2 are valid rectangles with a non-zero area"
        )
