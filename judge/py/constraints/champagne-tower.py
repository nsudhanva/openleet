"""Champagne Tower: cups poured and the queried glass."""


def check(poured: int, query_row: int, query_glass: int) -> None:
    assert 0 <= poured <= 10**9, "0 <= poured <= 10^9"
    assert 0 <= query_glass <= query_row < 100, "0 <= query_glass <= query_row < 100"
