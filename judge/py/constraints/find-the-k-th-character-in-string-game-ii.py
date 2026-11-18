"""Find the K-th Character in String Game II: a position k and a list of 0/1 operations."""


def check(k: int, operations: list[int]) -> None:
    assert isinstance(operations, list), "operations is an array"
    assert 1 <= k <= 10**14, "1 <= k <= 10^14"
    assert 1 <= len(operations) <= 100, "1 <= operations.length <= 100"
    assert all(op in (0, 1) for op in operations), "operations[i] is either 0 or 1"
    assert k <= 2 ** len(operations), "word has at least k characters after all operations"
