"""Count Houses at a Certain Distance I: n houses, plus an extra street x-y."""


def check(n: int, x: int, y: int) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert 1 <= x <= n, "1 <= x <= n"
    assert 1 <= y <= n, "1 <= y <= n"
