"""Allocate Mailboxes: distinct house positions and a mailbox count."""


def check(houses: list[int], k: int) -> None:
    assert 1 <= k <= len(houses) <= 100, "1 <= k <= houses.length <= 100"
    assert all(1 <= h <= 10**4 for h in houses), "1 <= houses[i] <= 10^4"
    assert len(set(houses)) == len(houses), "All the integers of houses are unique"
