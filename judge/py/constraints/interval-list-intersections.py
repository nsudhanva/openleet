"""Interval List Intersections: two sorted lists of disjoint closed intervals."""


def check(firstList: list[list[int]], secondList: list[list[int]]) -> None:
    for lst in (firstList, secondList):
        assert isinstance(lst, list), "interval lists are lists"
        assert 0 <= len(lst) <= 1000, "0 <= length <= 1000"
        assert all(isinstance(iv, list) and len(iv) == 2 for iv in lst), (
            "each interval is [start, end]"
        )
        assert all(0 <= s < e <= 10**9 for s, e in lst), "0 <= start < end <= 10^9"
        assert all(lst[i][1] < lst[i + 1][0] for i in range(len(lst) - 1)), (
            "intervals are disjoint and sorted: end_i < start_(i+1)"
        )
    assert len(firstList) + len(secondList) >= 1, "firstList.length + secondList.length >= 1"
