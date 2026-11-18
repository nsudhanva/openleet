"""Incremental Memory Leak: the free memory of two sticks."""


def check(memory1: int, memory2: int) -> None:
    assert 0 <= memory1 <= 2**31 - 1, "0 <= memory1 <= 2^31 - 1"
    assert 0 <= memory2 <= 2**31 - 1, "0 <= memory2 <= 2^31 - 1"
