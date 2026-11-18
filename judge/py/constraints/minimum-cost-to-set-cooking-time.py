"""Minimum Cost to Set Cooking Time: a start digit, move and push costs, target seconds."""


def check(startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> None:
    assert 0 <= startAt <= 9, "0 <= startAt <= 9"
    assert 1 <= moveCost <= 10**5, "1 <= moveCost <= 10^5"
    assert 1 <= pushCost <= 10**5, "1 <= pushCost <= 10^5"
    assert 1 <= targetSeconds <= 6039, "1 <= targetSeconds <= 6039"
