"""Minimum Cost Tree from Leaf Values: the in-order leaf values of a tree."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 40, "2 <= arr.length <= 40"
    assert all(1 <= x <= 15 for x in arr), "1 <= arr[i] <= 15"
    # With values <= 15 and 40 leaves the answer is far below 2^31, so the guarantee always holds.
