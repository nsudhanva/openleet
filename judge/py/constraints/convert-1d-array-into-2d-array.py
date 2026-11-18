"""Convert 1D Array Into 2D Array: a list of integers and target dimensions m x n."""


def check(original: list[int], m: int, n: int) -> None:
    assert isinstance(original, list), "original is a list"
    assert 1 <= len(original) <= 5 * 10**4, "1 <= original.length <= 5 * 10^4"
    assert all(isinstance(v, int) for v in original), "original[i] is an integer"
    assert all(1 <= v <= 10**5 for v in original), "1 <= original[i] <= 10^5"
    assert isinstance(m, int) and isinstance(n, int), "m and n are integers"
    assert 1 <= m <= 4 * 10**4, "1 <= m <= 4 * 10^4"
    assert 1 <= n <= 4 * 10**4, "1 <= n <= 4 * 10^4"
