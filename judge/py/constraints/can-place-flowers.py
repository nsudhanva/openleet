"""Can Place Flowers: a 0/1 flowerbed with no adjacent flowers, and a count n."""

from itertools import pairwise


def check(flowerbed: list[int], n: int) -> None:
    assert 1 <= len(flowerbed) <= 2 * 10**4, "1 <= flowerbed.length <= 2 * 10^4"
    assert all(v in (0, 1) for v in flowerbed), "flowerbed[i] is 0 or 1"
    assert not any(a and b for a, b in pairwise(flowerbed)), (
        "There are no two adjacent flowers in flowerbed"
    )
    assert 0 <= n <= len(flowerbed), "0 <= n <= flowerbed.length"
