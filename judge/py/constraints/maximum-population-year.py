"""Maximum Population Year: a list of [birth, death] years."""


def check(logs: list[list[int]]) -> None:
    assert 1 <= len(logs) <= 100, "1 <= logs.length <= 100"
    assert all(len(r) == 2 for r in logs), "logs[i].length == 2"
    assert all(1950 <= b < d <= 2050 for b, d in logs), "1950 <= birthi < deathi <= 2050"
