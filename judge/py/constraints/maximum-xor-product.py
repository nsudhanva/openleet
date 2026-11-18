"""Maximum Xor Product: two non-negative integers a, b below 2^50 and a bit count n."""


def check(a: int, b: int, n: int) -> None:
    assert isinstance(a, int) and isinstance(b, int) and isinstance(n, int), "integers"
    assert 0 <= a < 2**50, "0 <= a < 2^50"
    assert 0 <= b < 2**50, "0 <= b < 2^50"
    assert 0 <= n <= 50, "0 <= n <= 50"
