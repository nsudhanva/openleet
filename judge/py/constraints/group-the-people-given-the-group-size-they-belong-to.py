"""Group the People Given the Group Size They Belong To: each person's group size."""

from collections import Counter


def check(groupSizes: list[int]) -> None:
    n = len(groupSizes)
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(1 <= s <= n for s in groupSizes), "1 <= groupSizes[i] <= n"
    assert all(c % s == 0 for s, c in Counter(groupSizes).items()), (
        "there is at least one valid solution"
    )
