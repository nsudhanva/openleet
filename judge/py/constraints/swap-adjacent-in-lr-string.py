"""Swap Adjacent in LR String: two strings over L, R and X."""


def check(start: str, result: str) -> None:
    assert 1 <= len(start) <= 10**4, "1 <= start.length <= 10^4"
    assert len(start) == len(result), "start.length == result.length"
    assert set(start) <= set("LRX"), "start consists of 'L', 'R', 'X'"
    assert set(result) <= set("LRX"), "result consists of 'L', 'R', 'X'"
