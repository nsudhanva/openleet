"""Escape a Large Maze: blocked cells and two distinct unblocked points on a 10^6 grid."""


def check(blocked: list[list[int]], source: list[int], target: list[int]) -> None:
    lim = 10**6
    assert 0 <= len(blocked) <= 200, "0 <= blocked.length <= 200"
    assert all(isinstance(p, list) and len(p) == 2 for p in blocked), "blocked[i].length == 2"
    assert all(isinstance(v, int) and 0 <= v < lim for p in blocked for v in p), (
        "0 <= xi, yi < 10^6"
    )
    assert len(source) == 2 and len(target) == 2, "source.length == target.length == 2"
    assert all(isinstance(v, int) and 0 <= v < lim for v in source + target), (
        "0 <= sx, sy, tx, ty < 10^6"
    )
    assert source != target, "source != target"
    cells = {tuple(p) for p in blocked}
    assert tuple(source) not in cells, "source is not blocked"
    assert tuple(target) not in cells, "target is not blocked"
