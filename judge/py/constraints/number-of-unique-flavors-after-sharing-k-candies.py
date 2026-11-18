"""Number of Unique Flavors After Sharing K Candies: a list of candy flavors and k."""


def check(candies: list[int], k: int) -> None:
    assert isinstance(candies, list), "candies is a list"
    assert 0 <= len(candies) <= 10**5, "0 <= candies.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in candies), "1 <= candies[i] <= 10^5"
    assert 0 <= k <= len(candies), "0 <= k <= candies.length"
