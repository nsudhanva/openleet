"""Minimum Penalty for a Shop: a string of 'Y' and 'N'."""


def check(customers: str) -> None:
    assert 1 <= len(customers) <= 10**5, "1 <= customers.length <= 10^5"
    assert all(c in ("Y", "N") for c in customers), (
        "customers consists only of characters 'Y' and 'N'"
    )
