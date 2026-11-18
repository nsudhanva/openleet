"""Maximum Number That Sum of the Prices Is Less Than or Equal to K: a budget k and a bit step x."""


def check(k: int, x: int) -> None:
    assert 1 <= k <= 10**15, "1 <= k <= 10^15"
    assert 1 <= x <= 8, "1 <= x <= 8"
