"""Maximum Coins From K Consecutive Bags: non-overlapping [l, r, c] segments and k."""


def check(coins: list[list[int]], k: int) -> None:
    assert 1 <= len(coins) <= 10**5, "1 <= coins.length <= 10^5"
    assert all(len(c) == 3 for c in coins), "coins[i] == [li, ri, ci]"
    assert all(1 <= lo <= r <= 10**9 for lo, r, _ in coins), "1 <= li <= ri <= 10^9"
    assert all(1 <= c <= 1000 for _, _, c in coins), "1 <= ci <= 1000"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    segs = sorted((lo, r) for lo, r, _ in coins)
    assert all(segs[i][1] < segs[i + 1][0] for i in range(len(segs) - 1)), (
        "segments are non-overlapping"
    )
