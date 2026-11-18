"""Find the Winner of an Array Game: an array of distinct integers and k wins."""


def check(arr: list[int], k: int) -> None:
    assert 2 <= len(arr) <= 10**5, "2 <= arr.length <= 10^5"
    assert all(1 <= v <= 10**6 for v in arr), "1 <= arr[i] <= 10^6"
    assert len(set(arr)) == len(arr), "arr contains distinct integers"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
