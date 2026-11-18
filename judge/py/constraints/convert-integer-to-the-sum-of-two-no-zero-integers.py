"""Convert Integer to the Sum of Two No-Zero Integers: an integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
