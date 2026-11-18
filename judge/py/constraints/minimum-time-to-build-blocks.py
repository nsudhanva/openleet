"""Minimum Time to Build Blocks: block build times and a worker split cost."""


def check(blocks: list[int], split: int) -> None:
    assert 1 <= len(blocks) <= 1000, "1 <= blocks.length <= 1000"
    assert all(1 <= v <= 10**5 for v in blocks), "1 <= blocks[i] <= 10^5"
    assert 1 <= split <= 100, "1 <= split <= 100"
