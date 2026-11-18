"""Find the Prefix Common Array of Two Arrays: two permutations of 1..n."""


def check(A: list[int], B: list[int]) -> None:
    n = len(A)
    assert 1 <= n <= 50, "1 <= A.length <= 50"
    assert len(B) == n, "A.length == B.length == n"
    assert all(1 <= v <= n for v in A), "1 <= A[i] <= n"
    assert all(1 <= v <= n for v in B), "1 <= B[i] <= n"
    assert sorted(A) == list(range(1, n + 1)), "A is a permutation of n integers"
    assert sorted(B) == list(range(1, n + 1)), "B is a permutation of n integers"
