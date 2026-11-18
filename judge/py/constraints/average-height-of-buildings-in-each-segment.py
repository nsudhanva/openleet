"""Average Height of Buildings in Each Segment: buildings [start, end, height]."""


def check(buildings: list[list[int]]) -> None:
    assert 1 <= len(buildings) <= 10**5, "1 <= buildings.length <= 10^5"
    assert all(len(b) == 3 for b in buildings), "buildings[i].length == 3"
    assert all(0 <= s < e <= 10**8 for s, e, _ in buildings), "0 <= start_i < end_i <= 10^8"
    assert all(1 <= h <= 10**5 for _, _, h in buildings), "1 <= height_i <= 10^5"
