"""Best Team With No Conflicts: parallel lists of player scores and ages."""


def check(scores: list[int], ages: list[int]) -> None:
    assert 1 <= len(scores) <= 1000, "1 <= scores.length <= 1000"
    assert len(scores) == len(ages), "scores.length == ages.length"
    assert all(1 <= s <= 10**6 for s in scores), "1 <= scores[i] <= 10^6"
    assert all(1 <= a <= 1000 for a in ages), "1 <= ages[i] <= 1000"
