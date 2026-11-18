"""Distribute Candies: an even-length list of candy types."""


def check(candyType: list[int]) -> None:
    n = len(candyType)
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert n % 2 == 0, "n is even"
    assert all(-(10**5) <= v <= 10**5 for v in candyType), "-10^5 <= candyType[i] <= 10^5"
