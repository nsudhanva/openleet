"""Maximize Subarrays After Removing One Conflicting Pair: n and conflicting pairs."""


def check(n: int, conflictingPairs: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(conflictingPairs) <= 2 * n, "1 <= conflictingPairs.length <= 2 * n"
    assert all(len(p) == 2 for p in conflictingPairs), "conflictingPairs[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in conflictingPairs), (
        "1 <= conflictingPairs[i][j] <= n"
    )
    assert all(a != b for a, b in conflictingPairs), (
        "conflictingPairs[i][0] != conflictingPairs[i][1]"
    )
