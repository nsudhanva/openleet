"""Can I Win: the largest choosable integer and a desired total."""


def check(maxChoosableInteger: int, desiredTotal: int) -> None:
    assert 1 <= maxChoosableInteger <= 20, "1 <= maxChoosableInteger <= 20"
    assert 0 <= desiredTotal <= 300, "0 <= desiredTotal <= 300"
