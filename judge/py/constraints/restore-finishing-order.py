"""Restore Finishing Order: a permutation of 1..n and a strictly increasing list of friends."""


def check(order: list[int], friends: list[int]) -> None:
    n = len(order)
    assert 1 <= n <= 100, "1 <= n == order.length <= 100"
    assert sorted(order) == list(range(1, n + 1)), "order is a permutation of 1..n"
    assert 1 <= len(friends) <= min(8, n), "1 <= friends.length <= min(8, n)"
    assert all(1 <= f <= n for f in friends), "1 <= friends[i] <= n"
    assert all(friends[i] < friends[i + 1] for i in range(len(friends) - 1)), (
        "friends is strictly increasing"
    )
