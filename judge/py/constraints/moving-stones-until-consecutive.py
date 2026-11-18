"""Moving Stones Until Consecutive: three distinct stone positions."""


def check(a: int, b: int, c: int) -> None:
    assert all(1 <= v <= 100 for v in (a, b, c)), "1 <= a, b, c <= 100"
    assert len({a, b, c}) == 3, "a, b, and c have different values"
