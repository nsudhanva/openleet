"""Kids With the Greatest Number of Candies: candy counts and extra candies."""


def check(candies: list[int], extraCandies: int) -> None:
    assert 2 <= len(candies) <= 100, "2 <= n <= 100"
    assert all(1 <= v <= 100 for v in candies), "1 <= candies[i] <= 100"
    assert 1 <= extraCandies <= 50, "1 <= extraCandies <= 50"
