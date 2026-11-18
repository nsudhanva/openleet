"""Count Good Triplets: an array and three bounds a, b, c."""


def check(arr: list[int], a: int, b: int, c: int) -> None:
    assert 3 <= len(arr) <= 100, "3 <= arr.length <= 100"
    assert all(0 <= v <= 1000 for v in arr), "0 <= arr[i] <= 1000"
    assert 0 <= a <= 1000 and 0 <= b <= 1000 and 0 <= c <= 1000, "0 <= a, b, c <= 1000"
