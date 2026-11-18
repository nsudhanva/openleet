"""Statistics from a Large Sample: counts of each value 0..255 with a unique mode."""


def check(count: list[int]) -> None:
    assert len(count) == 256, "count.length == 256"
    assert all(0 <= c <= 10**9 for c in count), "0 <= count[i] <= 10^9"
    assert 1 <= sum(count) <= 10**9, "1 <= sum(count) <= 10^9"
    assert count.count(max(count)) == 1, "the mode of the sample is unique"
