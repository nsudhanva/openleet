"""Escape The Ghosts: ghost positions and a target on an infinite grid."""


def check(ghosts: list[list[int]], target: list[int]) -> None:
    assert 1 <= len(ghosts) <= 100, "1 <= ghosts.length <= 100"
    assert all(isinstance(p, list) and len(p) == 2 for p in ghosts), "ghosts[i].length == 2"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for p in ghosts for v in p), (
        "-10^4 <= xi, yi <= 10^4"
    )
    assert len(target) == 2, "target.length == 2"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v in target), (
        "-10^4 <= xtarget, ytarget <= 10^4"
    )
