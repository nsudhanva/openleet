"""Minimum Recolors to Get K Consecutive Black Blocks: a string of 'W'/'B' and a length k."""


def check(blocks: str, k: int) -> None:
    n = len(blocks)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(c in ("W", "B") for c in blocks), "blocks[i] is either 'W' or 'B'"
    assert 1 <= k <= n, "1 <= k <= n"
