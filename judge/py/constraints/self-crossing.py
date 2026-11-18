"""Self Crossing: a list of positive step distances."""


def check(distance: list[int]) -> None:
    assert 1 <= len(distance) <= 10**5, "1 <= distance.length <= 10^5"
    assert all(1 <= d <= 10**5 for d in distance), "1 <= distance[i] <= 10^5"
