"""Distance Between Bus Stops: distances around a circular route and two stops."""


def check(distance: list[int], start: int, destination: int) -> None:
    n = len(distance)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 0 <= start < n, "0 <= start < n"
    assert 0 <= destination < n, "0 <= destination < n"
    assert all(0 <= d <= 10**4 for d in distance), "0 <= distance[i] <= 10^4"
