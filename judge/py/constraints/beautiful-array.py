"""Beautiful Array: one integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
