"""Perfect Squares: one integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
