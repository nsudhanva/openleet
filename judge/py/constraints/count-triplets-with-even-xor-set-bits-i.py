"""Count Triplets with Even XOR Set Bits I: three arrays of small non-negative integers."""


def check(a: list[int], b: list[int], c: list[int]) -> None:
    assert all(isinstance(x, list) for x in (a, b, c)), "a, b, c are lists"
    assert all(1 <= len(x) <= 100 for x in (a, b, c)), "1 <= a.length, b.length, c.length <= 100"
    assert all(0 <= v <= 100 for x in (a, b, c) for v in x), "0 <= a[i], b[i], c[i] <= 100"
