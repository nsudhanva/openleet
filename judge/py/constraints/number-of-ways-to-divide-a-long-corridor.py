"""Number of Ways to Divide a Long Corridor: a string of seats 'S' and plants 'P'."""


def check(corridor: str) -> None:
    assert isinstance(corridor, str), "corridor is a string"
    assert 1 <= len(corridor) <= 10**5, "1 <= n <= 10^5"
    assert set(corridor) <= {"S", "P"}, "corridor[i] is either 'S' or 'P'"
