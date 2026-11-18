"""Number of Flowers in Full Bloom: [start, end] bloom intervals and arrival times."""


def check(flowers: list[list[int]], people: list[int]) -> None:
    assert 1 <= len(flowers) <= 5 * 10**4, "1 <= flowers.length <= 5 * 10^4"
    assert all(len(f) == 2 for f in flowers), "flowers[i].length == 2"
    assert all(1 <= s <= e <= 10**9 for s, e in flowers), "1 <= start_i <= end_i <= 10^9"
    assert 1 <= len(people) <= 5 * 10**4, "1 <= people.length <= 5 * 10^4"
    assert all(1 <= p <= 10**9 for p in people), "1 <= people[i] <= 10^9"
