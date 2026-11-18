"""Validate Binary Tree Nodes: n nodes with leftChild and rightChild index arrays."""


def check(n: int, leftChild: list[int], rightChild: list[int]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert len(leftChild) == n and len(rightChild) == n, (
        "n == leftChild.length == rightChild.length"
    )
    assert all(-1 <= v <= n - 1 for v in leftChild), "-1 <= leftChild[i] <= n - 1"
    assert all(-1 <= v <= n - 1 for v in rightChild), "-1 <= rightChild[i] <= n - 1"
