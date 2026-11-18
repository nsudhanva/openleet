"""Fair Candy Swap: two lists of candy box sizes with different totals and a valid swap."""


def check(aliceSizes: list[int], bobSizes: list[int]) -> None:
    assert 1 <= len(aliceSizes) <= 10**4, "1 <= aliceSizes.length <= 10^4"
    assert 1 <= len(bobSizes) <= 10**4, "1 <= bobSizes.length <= 10^4"
    assert all(1 <= x <= 10**5 for x in aliceSizes), "1 <= aliceSizes[i] <= 10^5"
    assert all(1 <= x <= 10**5 for x in bobSizes), "1 <= bobSizes[j] <= 10^5"
    sa, sb = sum(aliceSizes), sum(bobSizes)
    assert sa != sb, "Alice and Bob have a different total number of candies"
    assert (sb - sa) % 2 == 0, "there is at least one valid answer"
    diff = (sb - sa) // 2
    bob = set(bobSizes)
    assert any(a + diff in bob for a in aliceSizes), "there is at least one valid answer"
