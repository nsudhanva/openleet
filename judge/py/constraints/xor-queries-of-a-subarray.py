"""XOR Queries of a Subarray: an array and [left, right] queries."""


def check(arr: list[int], queries: list[list[int]]) -> None:
    n = len(arr)
    assert 1 <= n <= 3 * 10**4, "1 <= arr.length <= 3 * 10^4"
    assert 1 <= len(queries) <= 3 * 10**4, "1 <= queries.length <= 3 * 10^4"
    assert all(1 <= v <= 10**9 for v in arr), "1 <= arr[i] <= 10^9"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= a <= b < n for a, b in queries), "0 <= lefti <= righti < arr.length"
