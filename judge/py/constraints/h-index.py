"""H-Index: an array of citation counts."""


def check(citations: list[int]) -> None:
    n = len(citations)
    assert 1 <= n <= 5000, "1 <= n <= 5000"
    assert all(0 <= c <= 1000 for c in citations), "0 <= citations[i] <= 1000"
