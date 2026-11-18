"""Maximize Value of Function in a Ball Passing Game: receiver array and k passes."""


def check(receiver: list[int], k: int) -> None:
    n = len(receiver)
    assert 1 <= n <= 10**5, "1 <= receiver.length == n <= 10^5"
    assert all(0 <= v <= n - 1 for v in receiver), "0 <= receiver[i] <= n - 1"
    assert 1 <= k <= 10**10, "1 <= k <= 10^10"
