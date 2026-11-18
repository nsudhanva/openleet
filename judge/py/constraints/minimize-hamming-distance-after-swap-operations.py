"""Minimize Hamming Distance After Swap Operations: source, target and allowed swap index pairs."""


def check(source: list[int], target: list[int], allowedSwaps: list[list[int]]) -> None:
    n = len(source)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(target) == n, "source.length == target.length"
    assert all(1 <= v <= 10**5 for v in source), "1 <= source[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in target), "1 <= target[i] <= 10^5"
    assert 0 <= len(allowedSwaps) <= 10**5, "0 <= allowedSwaps.length <= 10^5"
    assert all(len(s) == 2 for s in allowedSwaps), "allowedSwaps[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in allowedSwaps), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in allowedSwaps), "ai != bi"
