"""Number of Ways to Paint N x 3 Grid: the number of rows."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 5000, "1 <= n <= 5000"
