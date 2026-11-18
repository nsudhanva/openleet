"""Count Triplets That Can Form Two Arrays of Equal XOR: an array of positive integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is a list"
    assert 1 <= len(arr) <= 300, "1 <= arr.length <= 300"
    assert all(1 <= v <= 10**8 for v in arr), "1 <= arr[i] <= 10^8"
