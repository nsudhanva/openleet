"""Arithmetic Subarrays: an array and m range queries [l[i], r[i]]."""


def check(nums: list[int], l: list[int], r: list[int]) -> None:  # noqa: E741
    n, m = len(nums), len(l)
    assert m == len(r), "m == l.length == r.length"
    assert 2 <= n <= 500, "2 <= n <= 500"
    assert 1 <= m <= 500, "1 <= m <= 500"
    assert all(0 <= a < b < n for a, b in zip(l, r, strict=True)), "0 <= l[i] < r[i] < n"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
