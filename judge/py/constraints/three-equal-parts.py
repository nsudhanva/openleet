"""Three Equal Parts: a binary array."""


def check(arr: list[int]) -> None:
    assert 3 <= len(arr) <= 3 * 10**4, "3 <= arr.length <= 3 * 10^4"
    assert all(x in (0, 1) for x in arr), "arr[i] is 0 or 1"
