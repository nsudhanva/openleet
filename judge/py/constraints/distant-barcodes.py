"""Distant Barcodes: a list of barcodes that can be rearranged so no two neighbours match."""

from collections import Counter


def check(barcodes: list[int]) -> None:
    assert 1 <= len(barcodes) <= 10000, "1 <= barcodes.length <= 10000"
    assert all(1 <= b <= 10000 for b in barcodes), "1 <= barcodes[i] <= 10000"
    most = max(Counter(barcodes).values())
    assert most <= (len(barcodes) + 1) // 2, "an answer is guaranteed to exist"
