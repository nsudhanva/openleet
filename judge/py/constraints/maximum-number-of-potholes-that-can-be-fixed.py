"""Maximum Number of Potholes That Can Be Fixed: a road of '.' and 'x' and a budget."""


def check(road: str, budget: int) -> None:
    assert 1 <= len(road) <= 10**5, "1 <= road.length <= 10^5"
    assert all(c in ".x" for c in road), "road consists only of characters '.' and 'x'"
    assert 1 <= budget <= 10**5 + 1, "1 <= budget <= 10^5 + 1"
