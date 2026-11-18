"""Last Moment Before All Ants Fall Out of a Plank: plank length and two ant position lists."""


def check(n: int, left: list[int], right: list[int]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 0 <= len(left) <= n + 1, "0 <= left.length <= n + 1"
    assert 0 <= len(right) <= n + 1, "0 <= right.length <= n + 1"
    assert all(0 <= v <= n for v in left), "0 <= left[i] <= n"
    assert all(0 <= v <= n for v in right), "0 <= right[i] <= n"
    assert 1 <= len(left) + len(right) <= n + 1, "1 <= left.length + right.length <= n + 1"
    assert len(set(left) | set(right)) == len(left) + len(right), (
        "all values of left and right are unique, each in only one array"
    )
