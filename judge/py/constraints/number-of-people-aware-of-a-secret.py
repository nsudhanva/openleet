"""Number of People Aware of a Secret: days n, delay and forget."""


def check(n: int, delay: int, forget: int) -> None:
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 1 <= delay < forget <= n, "1 <= delay < forget <= n"
