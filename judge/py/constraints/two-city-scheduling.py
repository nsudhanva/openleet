"""Two City Scheduling: 2n people, each with a cost for city A and city B."""


def check(costs: list[list[int]]) -> None:
    assert 2 <= len(costs) <= 100, "2 <= costs.length <= 100"
    assert len(costs) % 2 == 0, "costs.length is even"
    assert all(len(c) == 2 for c in costs), "costs[i].length == 2"
    assert all(1 <= a <= 1000 and 1 <= b <= 1000 for a, b in costs), "1 <= aCosti, bCosti <= 1000"
