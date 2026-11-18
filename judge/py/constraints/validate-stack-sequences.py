"""Validate Stack Sequences: distinct pushed values and a popped permutation."""


def check(pushed: list[int], popped: list[int]) -> None:
    assert 1 <= len(pushed) <= 1000, "1 <= pushed.length <= 1000"
    assert all(0 <= v <= 1000 for v in pushed), "0 <= pushed[i] <= 1000"
    assert len(set(pushed)) == len(pushed), "all the elements of pushed are unique"
    assert len(popped) == len(pushed), "popped.length == pushed.length"
    assert sorted(popped) == sorted(pushed), "popped is a permutation of pushed"
