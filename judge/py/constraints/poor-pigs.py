"""Poor Pigs: buckets and two time limits."""


def check(buckets: int, minutesToDie: int, minutesToTest: int) -> None:
    assert 1 <= buckets <= 1000, "1 <= buckets <= 1000"
    assert 1 <= minutesToDie <= minutesToTest <= 100, "1 <= minutesToDie <= minutesToTest <= 100"
