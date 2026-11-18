"""Minimum Space Wasted From Packaging: package sizes and suppliers' distinct box sizes."""


def check(packages: list[int], boxes: list[list[int]]) -> None:
    assert 1 <= len(packages) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(boxes) <= 10**5, "1 <= m <= 10^5"
    assert all(1 <= p <= 10**5 for p in packages), "1 <= packages[i] <= 10^5"
    assert all(1 <= len(b) <= 10**5 for b in boxes), "1 <= boxes[j].length <= 10^5"
    assert sum(len(b) for b in boxes) <= 10**5, "sum(boxes[j].length) <= 10^5"
    assert all(1 <= v <= 10**5 for b in boxes for v in b), "1 <= boxes[j][k] <= 10^5"
    assert all(len(set(b)) == len(b) for b in boxes), "the elements in boxes[j] are distinct"
