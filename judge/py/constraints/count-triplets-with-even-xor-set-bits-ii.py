"""Count Triplets with Even XOR Set Bits II: three arrays of non-negative integers."""


def check(a: list[int], b: list[int], c: list[int]) -> None:
    assert all(isinstance(x, list) for x in (a, b, c)), "a, b, c are lists"
    assert all(1 <= len(x) <= 10**5 for x in (a, b, c)), "1 <= a.length, b.length, c.length <= 10^5"
    assert all(0 <= v <= 10**9 for x in (a, b, c) for v in x), "0 <= a[i], b[i], c[i] <= 10^9"
