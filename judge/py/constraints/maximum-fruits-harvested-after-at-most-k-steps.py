"""Maximum Fruits Harvested After at Most K Steps: fruits sorted by position, a start and k."""

from itertools import pairwise


def check(fruits: list[list[int]], startPos: int, k: int) -> None:
    assert 1 <= len(fruits) <= 10**5, "1 <= fruits.length <= 10^5"
    assert all(len(f) == 2 for f in fruits), "fruits[i].length == 2"
    assert 0 <= startPos <= 2 * 10**5, "0 <= startPos <= 2 * 10^5"
    assert all(0 <= p <= 2 * 10**5 for p, _ in fruits), "0 <= positioni <= 2 * 10^5"
    assert all(a[0] < b[0] for a, b in pairwise(fruits)), "positioni-1 < positioni"
    assert all(1 <= a <= 10**4 for _, a in fruits), "1 <= amounti <= 10^4"
    assert 0 <= k <= 2 * 10**5, "0 <= k <= 2 * 10^5"
