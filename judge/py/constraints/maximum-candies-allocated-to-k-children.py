"""Maximum Candies Allocated to K Children: candy pile sizes and k."""


def check(candies: list[int], k: int) -> None:
    assert 1 <= len(candies) <= 10**5, "1 <= candies.length <= 10^5"
    assert all(1 <= c <= 10**7 for c in candies), "1 <= candies[i] <= 10^7"
    assert 1 <= k <= 10**12, "1 <= k <= 10^12"
