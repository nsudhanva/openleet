"""Maximum Number of Groups Getting Fresh Donuts: a batch size and group sizes."""


def check(batchSize: int, groups: list[int]) -> None:
    assert 1 <= batchSize <= 9, "1 <= batchSize <= 9"
    assert 1 <= len(groups) <= 30, "1 <= groups.length <= 30"
    assert all(1 <= v <= 10**9 for v in groups), "1 <= groups[i] <= 10^9"
