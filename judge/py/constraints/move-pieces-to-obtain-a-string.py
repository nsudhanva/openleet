"""Move Pieces to Obtain a String: two equal-length strings of 'L', 'R' and '_'."""


def check(start: str, target: str) -> None:
    assert len(start) == len(target), "n == start.length == target.length"
    assert 1 <= len(start) <= 10**5, "1 <= n <= 10^5"
    assert set(start) <= set("LR_") and set(target) <= set("LR_"), (
        "start and target consist of the characters 'L', 'R', and '_'"
    )
