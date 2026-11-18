"""Count Collisions on a Road: a string of directions L, R, S."""


def check(directions: str) -> None:
    assert 1 <= len(directions) <= 10**5, "1 <= directions.length <= 10^5"
    assert all(c in ("L", "R", "S") for c in directions), "directions[i] is 'L', 'R' or 'S'"
