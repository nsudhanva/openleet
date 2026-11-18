"""Number of Ways to Build House of Cards: a card count."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 500, "1 <= n <= 500"
