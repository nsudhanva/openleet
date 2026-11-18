"""Stone Game IV: a stone count."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
