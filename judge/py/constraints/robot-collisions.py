"""Robot Collisions: robots with distinct positions, healths and directions."""


def check(positions: list[int], healths: list[int], directions: str) -> None:
    n = len(positions)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(healths) == n and len(directions) == n, (
        "positions.length == healths.length == directions.length"
    )
    assert all(1 <= p <= 10**9 for p in positions), "1 <= positions[i] <= 10^9"
    assert all(1 <= h <= 10**9 for h in healths), "1 <= healths[i] <= 10^9"
    assert all(c in "LR" for c in directions), "directions[i] is 'L' or 'R'"
    assert len(set(positions)) == n, "all values in positions are distinct"
