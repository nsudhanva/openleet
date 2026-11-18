"""Number of Ways of Cutting a Pizza: a grid of 'A' and '.' and a piece count k."""


def check(pizza: list[str], k: int) -> None:
    assert isinstance(pizza, list), "pizza is a list"
    rows = len(pizza)
    assert 1 <= rows <= 50, "1 <= rows <= 50"
    assert all(isinstance(r, str) for r in pizza), "pizza[i] is a string"
    cols = len(pizza[0])
    assert 1 <= cols <= 50, "1 <= cols <= 50"
    assert all(len(r) == cols for r in pizza), "cols == pizza[i].length"
    assert all(set(r) <= {"A", "."} for r in pizza), "pizza consists of 'A' and '.' only"
    assert 1 <= k <= 10, "1 <= k <= 10"
