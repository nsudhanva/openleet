"""Maximum Number of Eaten Apples: apples grown and days until they rot."""


def check(apples: list[int], days: list[int]) -> None:
    n = len(apples)
    assert len(days) == n, "n == apples.length == days.length"
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert all(0 <= v <= 2 * 10**4 for v in apples), "0 <= apples[i] <= 2 * 10^4"
    assert all(0 <= v <= 2 * 10**4 for v in days), "0 <= days[i] <= 2 * 10^4"
    assert all((a == 0) == (d == 0) for a, d in zip(apples, days, strict=True)), (
        "days[i] = 0 if and only if apples[i] = 0"
    )
