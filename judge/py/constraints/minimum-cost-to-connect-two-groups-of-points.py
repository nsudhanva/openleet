"""Minimum Cost to Connect Two Groups of Points: a size1 x size2 cost matrix."""


def check(cost: list[list[int]]) -> None:
    size1 = len(cost)
    assert 1 <= size1 <= 12, "1 <= size1 <= 12"
    size2 = len(cost[0])
    assert all(len(row) == size2 for row in cost), "size2 == cost[i].length"
    assert 1 <= size2 <= 12, "1 <= size2 <= 12"
    assert size1 >= size2, "size1 >= size2"
    assert all(0 <= v <= 100 for row in cost for v in row), "0 <= cost[i][j] <= 100"
