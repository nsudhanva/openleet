"""K Empty Slots: a permutation of 1..n (bulb turned on each day) and a gap k."""


def check(bulbs: list[int], k: int) -> None:
    n = len(bulbs)
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert sorted(bulbs) == list(range(1, n + 1)), "bulbs is a permutation of 1..n"
    assert 0 <= k <= 2 * 10**4, "0 <= k <= 2 * 10^4"
