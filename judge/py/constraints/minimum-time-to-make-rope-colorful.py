"""Minimum Time to Make Rope Colorful: a colors string and removal times."""


def check(colors: str, neededTime: list[int]) -> None:
    n = len(colors)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(neededTime) == n, "n == colors.length == neededTime.length"
    assert all("a" <= c <= "z" for c in colors), "colors contains only lowercase English letters"
    assert all(1 <= v <= 10**4 for v in neededTime), "1 <= neededTime[i] <= 10^4"
