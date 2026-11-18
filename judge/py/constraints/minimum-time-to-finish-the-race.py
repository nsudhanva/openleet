"""Minimum Time to Finish the Race: tires as [f, r], a change time, and a lap count."""


def check(tires: list[list[int]], changeTime: int, numLaps: int) -> None:
    assert 1 <= len(tires) <= 10**5, "1 <= tires.length <= 10^5"
    assert all(len(t) == 2 for t in tires), "tires[i].length == 2"
    assert all(1 <= f <= 10**5 for f, _ in tires), "1 <= fi <= 10^5"
    assert all(2 <= r <= 10**5 for _, r in tires), "2 <= ri <= 10^5"
    assert 1 <= changeTime <= 10**5, "1 <= changeTime <= 10^5"
    assert 1 <= numLaps <= 1000, "1 <= numLaps <= 1000"
