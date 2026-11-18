"""Maximum White Tiles Covered by a Carpet: non-overlapping [l, r] tile ranges and a length."""


def check(tiles: list[list[int]], carpetLen: int) -> None:
    assert 1 <= len(tiles) <= 5 * 10**4, "1 <= tiles.length <= 5 * 10^4"
    assert all(len(t) == 2 for t in tiles), "tiles[i].length == 2"
    assert all(1 <= lo <= hi <= 10**9 for lo, hi in tiles), "1 <= li <= ri <= 10^9"
    assert 1 <= carpetLen <= 10**9, "1 <= carpetLen <= 10^9"
    ordered = sorted(tiles)
    assert all(ordered[i][1] < ordered[i + 1][0] for i in range(len(ordered) - 1)), (
        "the tiles are non-overlapping"
    )
