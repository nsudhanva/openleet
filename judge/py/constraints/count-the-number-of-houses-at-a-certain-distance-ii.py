"""Count Houses at a Certain Distance II: n houses, plus an extra street x-y."""


def check(n: int, x: int, y: int) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= x <= n, "1 <= x <= n"
    assert 1 <= y <= n, "1 <= y <= n"
