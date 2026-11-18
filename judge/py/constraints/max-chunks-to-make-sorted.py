"""Max Chunks To Make Sorted: a permutation of 0..n-1."""


def check(arr: list[int]) -> None:
    n = len(arr)
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert all(0 <= v < n for v in arr), "0 <= arr[i] < n"
    assert len(set(arr)) == n, "all the elements of arr are unique"
