"""Maximum Score From Removing Stones: three pile sizes."""


def check(a: int, b: int, c: int) -> None:
    assert all(1 <= v <= 10**5 for v in (a, b, c)), "1 <= a, b, c <= 10^5"
