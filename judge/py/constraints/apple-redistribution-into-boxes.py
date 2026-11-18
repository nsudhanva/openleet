"""Apple Redistribution into Boxes: apple pack sizes and box capacities."""


def check(apple: list[int], capacity: list[int]) -> None:
    assert 1 <= len(apple) <= 50, "1 <= n == apple.length <= 50"
    assert 1 <= len(capacity) <= 50, "1 <= m == capacity.length <= 50"
    assert all(1 <= v <= 50 for v in apple), "1 <= apple[i] <= 50"
    assert all(1 <= v <= 50 for v in capacity), "1 <= capacity[i] <= 50"
    assert sum(apple) <= sum(capacity), "it's possible to redistribute packs of apples into boxes"
