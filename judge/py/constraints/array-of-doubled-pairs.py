"""Array of Doubled Pairs: an even-length integer array."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 3 * 10**4, "2 <= arr.length <= 3 * 10^4"
    assert len(arr) % 2 == 0, "arr.length is even"
    assert all(-(10**5) <= v <= 10**5 for v in arr), "-10^5 <= arr[i] <= 10^5"
