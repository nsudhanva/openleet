"""Count Number of Teams: distinct soldier ratings."""


def check(rating: list[int]) -> None:
    assert 3 <= len(rating) <= 1000, "3 <= n <= 1000"
    assert all(1 <= v <= 10**5 for v in rating), "1 <= rating[i] <= 10^5"
    assert len(set(rating)) == len(rating), "all the integers in rating are unique"
