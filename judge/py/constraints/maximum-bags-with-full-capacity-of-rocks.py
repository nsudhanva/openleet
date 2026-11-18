"""Maximum Bags With Full Capacity of Rocks: bag capacities, current rocks, extra rocks."""


def check(capacity: list[int], rocks: list[int], additionalRocks: int) -> None:
    n = len(capacity)
    assert n == len(rocks), "capacity.length == rocks.length"
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(1 <= c <= 10**9 for c in capacity), "1 <= capacity[i] <= 10^9"
    assert all(0 <= r <= c for r, c in zip(rocks, capacity, strict=True)), (
        "0 <= rocks[i] <= capacity[i]"
    )
    assert 1 <= additionalRocks <= 10**9, "1 <= additionalRocks <= 10^9"
