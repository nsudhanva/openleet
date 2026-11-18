"""Count and Say: a term index n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 30, "1 <= n <= 30"
