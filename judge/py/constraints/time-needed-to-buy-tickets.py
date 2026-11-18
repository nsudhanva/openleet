"""Time Needed to Buy Tickets: ticket counts per person and the index k of the target person."""


def check(tickets: list[int], k: int) -> None:
    n = len(tickets)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= t <= 100 for t in tickets), "1 <= tickets[i] <= 100"
    assert 0 <= k < n, "0 <= k < n"
